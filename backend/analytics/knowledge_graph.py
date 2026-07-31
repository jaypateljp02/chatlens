"""
Knowledge Graph Generator for ChatLens AI.
Uses NetworkX to map interconnected relationships between People, Topics, and Groups.
"""
from typing import List
from collections import defaultdict
import networkx as nx

from models.schemas import ParsedMessage


def generate_knowledge_graph(messages: List[ParsedMessage], group_name: str = "WhatsApp Group") -> dict:
    """Generate a rich node-edge graph structure using NetworkX."""
    G = nx.Graph()
    
    # 1. Add Group node (Center)
    G.add_node(
        group_name, 
        type="group", 
        size=32, 
        color="#128C7E", 
        message_count=len(messages), 
        details=f"Central Chat Group Entity with {len(messages)} messages.",
        sample_memory=f"Indexed {len(messages)} messages in persistent vector memory."
    )
    
    participants = defaultdict(int)
    person_peak_hours = defaultdict(lambda: defaultdict(int))
    person_sample_msgs = defaultdict(list)
    
    topics = {
        "Health & Pediatric Care": ["doctor", "fever", "medicine", "cough", "hospital", "taare", "health", "patient"],
        "Project & Delivery": ["proposal", "deadline", "project", "client", "release", "pdf", "deliver", "work"],
        "Training & Skills": ["workshop", "course", "python", "ai", "training", "program", "learn", "class"],
        "Operations & Setup": ["server", "postgres", "iis", "database", "install", "config", "setup", "network"]
    }
    
    topic_counts = defaultdict(int)
    person_topic_links = defaultdict(int)
    topic_sample_msgs = defaultdict(list)
    
    for msg in messages:
        if msg.is_system or not msg.sender:
            continue
        
        sender = msg.sender
        participants[sender] += 1
        hour = msg.timestamp.hour
        person_peak_hours[sender][hour] += 1

        text = msg.content
        if len(person_sample_msgs[sender]) < 3:
            person_sample_msgs[sender].append(f"[{msg.timestamp.strftime('%H:%M')}] {sender}: {text}")

        text_lower = text.lower()
        
        # Topic matching
        for topic_name, keywords in topics.items():
            if any(k in text_lower for k in keywords):
                topic_counts[topic_name] += 1
                person_topic_links[(sender, topic_name)] += 1
                if len(topic_sample_msgs[topic_name]) < 3:
                    topic_sample_msgs[topic_name].append(f"[{msg.timestamp.strftime('%H:%M')}] {sender}: {text}")
    
    # 2. Add Person nodes
    for person, count in participants.items():
        peak_h = max(person_peak_hours[person].items(), key=lambda x: x[1])[0] if person_peak_hours[person] else 12
        sample_mem = "\n".join(person_sample_msgs[person]) if person_sample_msgs[person] else f"Active participant with {count} msgs."
        G.add_node(
            person, 
            type="person", 
            size=min(18 + count // 10, 28), 
            color="#25D366",
            message_count=count,
            peak_hour=f"{peak_h:02d}:00",
            details=f"Active participant with {count} messages exchanged.",
            sample_memory=sample_mem
        )
        G.add_edge(group_name, person, weight=count, label="member_of")
    
    # 3. Add Topic nodes
    for topic, count in topic_counts.items():
        if count > 0:
            sample_mem = "\n".join(topic_sample_msgs[topic]) if topic_sample_msgs[topic] else f"Topic discussed in {count} msgs."
            G.add_node(
                topic, 
                type="topic", 
                size=min(18 + count // 5, 28), 
                color="#FF6D00",
                message_count=count,
                details=f"Topic discussed across {count} messages.",
                sample_memory=sample_mem
            )
            G.add_edge(group_name, topic, weight=count, label="discussed_in")
    
    # 4. Add Person <-> Topic edges
    for (person, topic), weight in person_topic_links.items():
        if weight >= 1:
            G.add_edge(person, topic, weight=weight, label="spoke_about")
    
    # Convert NetworkX graph to JSON dictionary for frontend rendering
    nodes = []
    for node, data in G.nodes(data=True):
        nodes.append({
            "id": node,
            "name": node,
            "type": data.get("type", "concept"),
            "size": data.get("size", 18),
            "color": data.get("color", "#53BDEB"),
            "message_count": data.get("message_count", 0),
            "peak_hour": data.get("peak_hour", "N/A"),
            "details": data.get("details", ""),
            "sample_memory": data.get("sample_memory", "")
        })
    
    edges = []
    for source, target, data in G.edges(data=True):
        edges.append({
            "source": source,
            "target": target,
            "weight": data.get("weight", 1),
            "label": data.get("label", "connected")
        })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }
