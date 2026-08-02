import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import { CheckCircle2, Clock } from 'lucide-react-native';
import { getActionItems } from '../api/client';

const ActionsScreen = () => {
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActions();
  }, []);

  const loadActions = async () => {
    try {
      const res = await getActionItems('all');
      setActions(res?.action_items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <View style={styles.iconBox}>
        {item.status === 'completed' ? (
          <CheckCircle2 size={24} color="#10b981" />
        ) : (
          <Clock size={24} color="#f59e0b" />
        )}
      </View>
      <View style={styles.content}>
        <Text style={styles.promise}>"{item.promise}"</Text>
        <View style={styles.meta}>
          <Text style={styles.assignee}>Owner: {item.assignee}</Text>
          <Text style={styles.date}>{new Date(item.detected_date).toLocaleDateString()}</Text>
        </View>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Pending Commitments</Text>
        <Text style={styles.subtitle}>Extracted directly from your chats.</Text>
      </View>
      
      {loading ? (
        <ActivityIndicator color="#6366f1" size="large" style={{ marginTop: 50 }} />
      ) : actions.length === 0 ? (
        <Text style={styles.empty}>No action items found.</Text>
      ) : (
        <FlatList
          data={actions}
          keyExtractor={(item, index) => index.toString()}
          renderItem={renderItem}
          contentContainerStyle={{ paddingBottom: 20 }}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f11', padding: 16 },
  header: { marginBottom: 20, marginTop: 10 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff', marginBottom: 4 },
  subtitle: { fontSize: 14, color: '#a1a1aa' },
  card: { backgroundColor: '#18181b', borderRadius: 12, padding: 16, marginBottom: 12, flexDirection: 'row', borderWidth: 1, borderColor: '#27272a' },
  iconBox: { marginRight: 16, justifyContent: 'center' },
  content: { flex: 1 },
  promise: { fontSize: 15, color: '#fff', marginBottom: 10, fontStyle: 'italic' },
  meta: { flexDirection: 'row', justifyContent: 'space-between' },
  assignee: { fontSize: 12, color: '#6366f1', fontWeight: 'bold' },
  date: { fontSize: 12, color: '#71717a' },
  empty: { color: '#a1a1aa', textAlign: 'center', marginTop: 40 },
});

export default ActionsScreen;
