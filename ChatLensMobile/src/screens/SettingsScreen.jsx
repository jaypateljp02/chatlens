import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Server, Smartphone, Lock } from 'lucide-react-native';

const SettingsScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Settings</Text>
      
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>AI Engine Connection</Text>
        
        <TouchableOpacity style={[styles.option, styles.optionActive]}>
          <Server color="#6366f1" size={20} />
          <View style={styles.optionTextContainer}>
            <Text style={styles.optionTitle}>Gemini 3.6 Flash (Live Cloud)</Text>
            <Text style={styles.optionSubtitle}>Maximum intelligence & speed</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.option}>
          <Smartphone color="#a1a1aa" size={20} />
          <View style={styles.optionTextContainer}>
            <Text style={[styles.optionTitle, { color: '#a1a1aa' }]}>Gemma Local (Offline Mode)</Text>
            <Text style={styles.optionSubtitle}>Requires model download (coming soon)</Text>
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Privacy</Text>
        <TouchableOpacity style={styles.option}>
          <Lock color="#a1a1aa" size={20} />
          <View style={styles.optionTextContainer}>
            <Text style={[styles.optionTitle, { color: '#a1a1aa' }]}>Clear Local Vault</Text>
            <Text style={styles.optionSubtitle}>Deletes all imported chats from this device</Text>
          </View>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f11', padding: 20 },
  title: { fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 30 },
  section: { marginBottom: 30 },
  sectionTitle: { fontSize: 13, fontWeight: 'bold', color: '#71717a', textTransform: 'uppercase', marginBottom: 12, letterSpacing: 1 },
  option: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#18181b', padding: 16, borderRadius: 12, marginBottom: 10, borderWidth: 1, borderColor: '#27272a' },
  optionActive: { borderColor: '#6366f1', backgroundColor: '#6366f110' },
  optionTextContainer: { marginLeft: 16 },
  optionTitle: { color: '#fff', fontSize: 16, fontWeight: '600' },
  optionSubtitle: { color: '#71717a', fontSize: 12, marginTop: 4 },
});

export default SettingsScreen;
