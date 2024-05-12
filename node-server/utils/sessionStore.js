// utils/sessionStore.js

class SessionStore {
    constructor() {
        this.sessions = new Map();
    }

    getSession(sessionId) {
        return this.sessions.get(sessionId);
    }

    setSession(sessionId, sessionData) {
        this.sessions.set(sessionId, sessionData);
    }

    deleteSession(sessionId) {
        this.sessions.delete(sessionId);
    }
}

const sessionStore = new SessionStore();

export default sessionStore;
