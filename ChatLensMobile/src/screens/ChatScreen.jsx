import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
import { Send, Bot } from 'lucide-react-native';
import { askQuestion } from '../api/client';

const ChatScreen = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { type: 'ai', text: 'Hi! Ask me anything about your uploaded WhatsApp chats. I use Gemini 3.6 Flash to give you answers based directly on your messages.' }
  ]);

  const handleSend = async () => {
    if (!query.trim()) return;
    const userMsg = query;
    setMessages(prev => [...prev, { type: 'user', text: userMsg }]);
    setQuery('');
    setLoading(true);

    try {
      const res = await askQuestion('all', userMsg);
      setMessages(prev => [
        ...prev, 
        { type: 'ai', text: res.answer, sources: res.source_messages }
      ]);
    } catch (err) {
      setMessages(prev => [...prev, { type: 'ai', text: 'Error connecting to AI backend.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.chatArea} contentContainerStyle={{ paddingBottom: 20 }}>
        {messages.map((msg, idx) => (
          <View key={idx} style={[styles.bubble, msg.type === 'user' ? styles.userBubble : styles.aiBubble]}>
            {msg.type === 'ai' && <View style={styles.botIcon}><Bot size={16} color="#fff" /></View>}
            <View style={styles.messageContent}>
              <Text style={styles.messageText}>{msg.text}</Text>
              
              {/* Show source references if returned */}
              {msg.sources && msg.sources.length > 0 && (
                <View style={styles.sourcesContainer}>
                  <Text style={styles.sourceTitle}>Source References:</Text>
                  {msg.sources.map((src, i) => (
                    <View key={i} style={styles.sourceQuote}>
                      <Text style={styles.sourceText}>{src}</Text>
                    </View>
                  ))}
                </View>
              )}
            </View>
          </View>
        ))}
        {loading && <ActivityIndicator color="#6366f1" style={{ marginTop: 20 }} />}
      </ScrollView>

      <View style={styles.inputArea}>
        <TextInput
          style={styles.input}
          placeholder="Ask a question..."
          placeholderTextColor="#71717a"
          value={query}
          onChangeText={setQuery}
          onSubmitEditing={handleSend}
        />
        <TouchableOpacity style={styles.sendBtn} onPress={handleSend} disabled={loading}>
          <Send size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f11' },
  chatArea: { flex: 1, padding: 16 },
  bubble: { maxWidth: '85%', marginBottom: 16, borderRadius: 16, padding: 14, flexDirection: 'row' },
  userBubble: { alignSelf: 'flex-end', backgroundColor: '#6366f1' },
  aiBubble: { alignSelf: 'flex-start', backgroundColor: '#18181b', borderWidth: 1, borderColor: '#27272a' },
  botIcon: { width: 28, height: 28, borderRadius: 14, backgroundColor: '#3f3f46', alignItems: 'center', justifyContent: 'center', marginRight: 10, marginTop: 2 },
  messageContent: { flex: 1 },
  messageText: { color: '#fff', fontSize: 15, lineHeight: 22 },
  sourcesContainer: { marginTop: 12, paddingTop: 12, borderTopWidth: 1, borderTopColor: '#3f3f46' },
  sourceTitle: { color: '#a1a1aa', fontSize: 12, fontWeight: 'bold', marginBottom: 6 },
  sourceQuote: { backgroundColor: '#27272a', padding: 8, borderRadius: 8, marginBottom: 4, borderLeftWidth: 3, borderLeftColor: '#6366f1' },
  sourceText: { color: '#d4d4d8', fontSize: 12, fontStyle: 'italic' },
  inputArea: { flexDirection: 'row', padding: 16, backgroundColor: '#18181b', borderTopWidth: 1, borderTopColor: '#27272a', alignItems: 'center' },
  input: { flex: 1, backgroundColor: '#27272a', borderRadius: 24, paddingHorizontal: 16, paddingVertical: 12, color: '#fff', fontSize: 15 },
  sendBtn: { backgroundColor: '#6366f1', width: 44, height: 44, borderRadius: 22, alignItems: 'center', justifyContent: 'center', marginLeft: 12 },
});

export default ChatScreen;
