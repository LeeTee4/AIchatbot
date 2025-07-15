const API_BASE_URL = "http://127.0.0.1:8000";

export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

export interface ChatResponse {
  answer: string;
}

export interface ChatError {
  error: string;
}

export interface TestResponse {
  message: string;
  timestamp: number;
  gemini_configured: boolean;
}

export class ApiService {
  static async sendMessage(question: string): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("API endpoint not found. Make sure the Django server is running on port 8000.");
        }
        
        const errorText = await response.text();
        let errorData: ChatError;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { error: `HTTP ${response.status}: ${errorText}` };
        }
        
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      return data.answer;
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to send message: ${error.message}`);
      }
      throw new Error("Failed to send message: Unknown error");
    }
  }

  static async testConnection(): Promise<boolean> {
    try {
      // First try a simple test message to the chat endpoint
      const testResponse = await fetch(`${API_BASE_URL}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: "test" }),
      });
      
      if (testResponse.ok) {
        return true;
      }

      // If that fails, try the test endpoint
      const backupResponse = await fetch(`${API_BASE_URL}/api/test/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      return backupResponse.ok;
    } catch (error) {
      console.error("Connection test failed:", error);
      return false;
    }
  }

  static async getBackendStatus(): Promise<TestResponse | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/test/`, {
        method: "GET",
      });
      
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch {
      return null;
    }
  }

  static async testEcho(message: string): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/test/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: message }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.response || "Echo test successful";
      }
      throw new Error("Echo test failed");
    } catch (error) {
      throw new Error(`Echo test failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }
}
