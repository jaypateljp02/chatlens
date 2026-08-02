import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import DocumentPicker from 'react-native-document-picker';
import { UploadCloud, MessageCircle, Users } from 'lucide-react-native';
import { uploadChat } from '../api/client';

const HomeScreen = () => {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ messages: 0, participants: 0 });

  const handleUpload = async () => {
    try {
      const res = await DocumentPicker.pickSingle({
        type: [DocumentPicker.types.plainText],
      });
      setLoading(true);
      const result = await uploadChat(res);
      setStats({
        messages: result.metadata?.total_messages || 0,
        participants: result.metadata?.participants?.length || 0,
      });
      Alert.alert('Success', 'Chat uploaded and analyzed successfully!');
    } catch (err) {
      if (!DocumentPicker.isCancel(err)) {
        Alert.alert('Error', 'Failed to upload chat.');
        console.error(err);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Welcome to ChatLens AI</Text>
        <Text style={styles.subtitle}>Upload a WhatsApp export to extract insights.</Text>
      </View>

      <TouchableOpacity style={styles.uploadCard} onPress={handleUpload} disabled={loading}>
        <UploadCloud size={40} color="#6366f1" />
        <Text style={styles.uploadText}>{loading ? 'Uploading & Analyzing...' : 'Tap to Upload Chat (.txt)'}</Text>
      </TouchableOpacity>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <MessageCircle size={24} color="#10b981" />
          <Text style={styles.statNumber}>{stats.messages}</Text>
          <Text style={styles.statLabel}>Messages Analyzed</Text>
        </View>
        <View style={styles.statCard}>
          <Users size={24} color="#f59e0b" />
          <Text style={styles.statNumber}>{stats.participants}</Text>
          <Text style={styles.statLabel}>Participants</Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f11', padding: 20 },
  header: { marginBottom: 30, marginTop: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#fff', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#a1a1aa' },
  uploadCard: {
    backgroundColor: '#18181b',
    borderWidth: 1,
    borderColor: '#27272a',
    borderRadius: 16,
    padding: 40,
    alignItems: 'center',
    marginBottom: 30,
    borderStyle: 'dashed',
  },
  uploadText: { color: '#6366f1', marginTop: 16, fontSize: 16, fontWeight: '600' },
  statsContainer: { flexDirection: 'row', justifyContent: 'space-between' },
  statCard: {
    backgroundColor: '#18181b',
    borderRadius: 16,
    padding: 20,
    width: '48%',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#27272a',
  },
  statNumber: { fontSize: 24, fontWeight: 'bold', color: '#fff', marginTop: 12 },
  statLabel: { fontSize: 12, color: '#a1a1aa', marginTop: 4 },
});

export default HomeScreen;
