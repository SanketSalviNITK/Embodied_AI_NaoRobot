import React, { useState, useEffect, useRef } from 'react';
import { Camera, Send, Loader2 } from 'lucide-react';

const VQASandbox = () => {
  const [frameUrl, setFrameUrl] = useState(null);
  const [chatLog, setChatLog] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Poll the camera frame from the AI orchestrator
    const interval = setInterval(() => {
      fetch('http://localhost:5002/stream_frame')
        .then(res => res.json())
        .then(data => {
          if (data.status === 'ok' && data.image) {
            setFrameUrl(`data:image/jpeg;base64,${data.image}`);
          }
        })
        .catch(err => console.error("Error polling frame", err));
    }, 1000); // 1 FPS for testing
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatLog, isThinking]);

  const handleSend = async () => {
    if (!inputValue.trim() || isThinking) return;
    
    const msg = inputValue.trim();
    setChatLog(prev => [...prev, { role: 'user', text: msg }]);
    setInputValue("");
    setIsThinking(true);

    try {
      const res = await fetch('http://localhost:5002/vqa_chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const data = await res.json();
      if (data.status === 'success') {
        setChatLog(prev => [...prev, { role: 'robot', text: data.reply }]);
      } else {
        setChatLog(prev => [...prev, { role: 'robot', text: `[Error] ${data.reply || data.message}` }]);
      }
    } catch (err) {
      setChatLog(prev => [...prev, { role: 'robot', text: '[Network Error] Failed to reach Brain (port 5002).' }]);
    }
    
    setIsThinking(false);
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in zoom-in-95 duration-700">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left Side: Camera Feed */}
        <div className="glass-card bg-slate-950/60 border-accent/20 flex flex-col p-6 rounded-lg relative overflow-hidden">
          <div className="flex items-center gap-2 text-accent mb-4 uppercase text-xs tracking-widest font-bold">
            <Camera size={14} /> Live Vision Matrix
          </div>
          <div className="aspect-video bg-black rounded border border-slate-800 flex items-center justify-center overflow-hidden">
            {frameUrl ? (
              <img src={frameUrl} alt="NAO Vision" className="w-full h-full object-cover" />
            ) : (
              <div className="flex flex-col items-center text-slate-500 gap-2">
                <Loader2 className="animate-spin" size={24} />
                <span className="text-xs uppercase tracking-widest">Waiting for stream...</span>
              </div>
            )}
          </div>
        </div>

        {/* Right Side: VQA Chat */}
        <div className="glass-card bg-slate-950/60 border-primary/20 flex flex-col p-6 rounded-lg h-[400px]">
          <div className="text-primary mb-4 uppercase text-xs tracking-widest font-bold">
            Visual QA Sandbox
          </div>
          
          <div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-2 custom-scrollbar">
            {chatLog.length === 0 && (
              <div className="text-slate-500 text-xs text-center mt-10">
                Ask NAO about what it currently sees, or say "Register my face as [Name]".
              </div>
            )}
            {chatLog.map((c, i) => (
              <div key={i} className={`flex ${c.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded p-3 text-sm ${
                  c.role === 'user' 
                    ? 'bg-primary/20 text-white border border-primary/30 rounded-br-none' 
                    : 'bg-slate-800/80 text-slate-200 border border-slate-700 rounded-bl-none'
                }`}>
                  {c.text}
                </div>
              </div>
            ))}
            {isThinking && (
              <div className="flex justify-start">
                <div className="bg-slate-800/80 border border-slate-700 text-slate-400 p-3 rounded rounded-bl-none text-xs flex items-center gap-2">
                  <Loader2 className="animate-spin" size={12} /> Analyzing vision...
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="mt-4 flex gap-2">
            <input 
              type="text" 
              className="flex-1 bg-black/50 border border-slate-800 text-white px-4 py-2 rounded focus:outline-none focus:border-primary transition-colors text-sm"
              placeholder="E.g. What do you see right now?"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button 
              className="bg-primary/20 hover:bg-primary/40 border border-primary/50 text-primary px-4 py-2 rounded transition-all"
              onClick={handleSend}
            >
              <Send size={16} />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default VQASandbox;
