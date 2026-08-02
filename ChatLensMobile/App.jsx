import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, MessageSquare, CheckCircle, Settings } from 'lucide-react-native';

// Import Screens
import HomeScreen from './src/screens/HomeScreen';
import ChatScreen from './src/screens/ChatScreen';
import ActionsScreen from './src/screens/ActionsScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          headerStyle: {
            backgroundColor: '#121212',
            borderBottomWidth: 1,
            borderBottomColor: '#2C2C2C',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
          tabBarStyle: {
            backgroundColor: '#121212',
            borderTopWidth: 1,
            borderTopColor: '#2C2C2C',
            paddingBottom: 5,
            height: 60,
          },
          tabBarActiveTintColor: '#6366f1',
          tabBarInactiveTintColor: '#888',
          tabBarIcon: ({ color, size }) => {
            let IconComponent;
            if (route.name === 'Dashboard') IconComponent = Home;
            else if (route.name === 'Chat') IconComponent = MessageSquare;
            else if (route.name === 'Actions') IconComponent = CheckCircle;
            else if (route.name === 'Settings') IconComponent = Settings;
            return <IconComponent color={color} size={size} />;
          },
        })}
      >
        <Tab.Screen name="Dashboard" component={HomeScreen} options={{ title: 'ChatLens Dashboard' }} />
        <Tab.Screen name="Chat" component={ChatScreen} options={{ title: 'Ask AI' }} />
        <Tab.Screen name="Actions" component={ActionsScreen} options={{ title: 'Action Items' }} />
        <Tab.Screen name="Settings" component={SettingsScreen} options={{ title: 'Settings' }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

export default App;
