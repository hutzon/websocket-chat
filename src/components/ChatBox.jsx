import React, { useEffect, useRef, useState } from "react";

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const myConnectionIdRef = useRef(null);

  const socketRef = useRef(null);

  const WS_URL =
    "wss://tuusuario.execute-api.us-east-1.amazonaws.com/production/";

  useEffect(() => {
    socketRef.current = new WebSocket(WS_URL);

    socketRef.current.onopen = () => {
      console.log("WebSocket conectado");
    };

    socketRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.connectionId) {
          myConnectionIdRef.current =
            myConnectionIdRef.current || data.connectionId;
        }

        if (data.message) {
          const isMine = data.from === myConnectionIdRef.current;
          setMessages((prev) => [
            ...prev,
            `${isMine ? "🧑 Tu" : "📨"} : ${data.message}`,
          ]);
        }
      } catch (error) {
        console.error("Error parsing message", error);
      }
    };
    socketRef.current.onclose = () => {
      console.log("WebSocket cerrado");
    };

    return () => {
      socketRef.current.close();
    };
  }, []);

  const sendMessage = () => {
    if (
      input.trim() !== "" &&
      socketRef.current.readyState === WebSocket.OPEN
    ) {
      const message = {
        action: "send_message", // este es el nombre de su metodo en websocket
        data: input,
      };

      socketRef.current.send(JSON.stringify(message));
      setInput("");
    }
  };

  const closeConnection = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.close();
      console.log("Conexión cerrada");
    }
  };

  return (
    <div>
      <h1>WebSocket API</h1>
      <div
        style={{
          border: "1px solid #ccc",
          padding: 10,
          height: 200,
          overflowY: "scroll",
          marginBottom: 10,
        }}
      >
        {messages.map((msg, idx) => (
          <div key={idx}>{msg}</div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Escribe un mensaje..."
      />
      <button onClick={sendMessage}>Enviar</button>
      <button onClick={closeConnection}>Cerrar conexion</button>
    </div>
  );
}

export default ChatBox;
