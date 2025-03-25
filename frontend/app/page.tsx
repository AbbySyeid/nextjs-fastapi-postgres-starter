"use client";

import { useState, useEffect, useRef } from "react";

type User = { id: string; name: string };
type Message = { id: number; user_id: number; content: string };

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [user, setUser] = useState<User | null>(null);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const fetchUser = async () => {
    const response = await fetch(`${apiUrl}/users/me`);
    const userData: User = await response.json();
    setUser(userData);
  };

  const fetchMessages = async () => {
    const response = await fetch(`${apiUrl}/messages/`);
    const data = await response.json();
    setMessages(data);
  };

  const sendMessage = async () => {
    if (!input.trim() || !user) return;

    await fetch(`${apiUrl}/messages/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: user.id, content: input }),
    });

    setInput("");
    fetchMessages();
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") sendMessage();
  };

  useEffect(() => {
    if (messagesEndRef.current) messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    fetchUser();
    fetchMessages();
  }, []);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen w-screen">
      {user && <h1 className="text-2xl font-bold mb-4">Hello, {user.name}!</h1>}
      <div className="chat-box w-full p-9 mx-4 rounded-lg shadow-md flex flex-col h-full">
        <div className="messages mb-4 max-h-[calc(100vh-200px)] overflow-y-scroll">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.user_id === user?.id ? "justify-end" : "justify-start"}`}>
              <div className={`message rounded-lg p-2 my-2 max-w-[calc(100vw/2)] ${msg.user_id === user?.id ? "bg-blue-500" : "bg-red-500"}`}>
                <div className="message-content p-1">
                  {msg.content}
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="flex items-center space-x-2 mt-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type a message..."
            className="input-field p-2 w-full text-black border rounded-lg"
          />
          <button
            onClick={sendMessage}
            className="send-button p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700"
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}
