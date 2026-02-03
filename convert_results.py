import json
import os

def convert_to_markdown(json_file="bio_eval_results.json", output_file="conversation_log.md"):
    if not os.path.exists(json_file):
        print(f"File {json_file} not found.")
        return

    with open(json_file, "r") as f:
        data = json.load(f)

    with open(output_file, "w") as f:
        f.write("# Bio-Eval Conversation Log\n\n")
        
        current_track = None
        
        for entry in data:
            track = entry.get("track_id", "Unknown Track")
            turn = entry.get("turn_index", "?")
            role = entry.get("model_role", "Unknown Role")
            content = entry.get("content", "")
            latency = entry.get("response_latency_ms", 0)
            refusal = entry.get("refusal_detected", False)
            
            # Header for new track
            if track != current_track:
                f.write(f"\n## {track}\n\n")
                current_track = track
            
            # Check for new schema (paired) vs old schema (single role)
            if "attacker_prompt" in entry:
                # New Schema
                f.write(f"### Turn {turn}\n")
                f.write(f"**Latency:** {latency:.2f} ms | **Refusal:** {'YES' if refusal else 'NO'}\n\n")
                
                f.write(f"#### 🔵 Attacker Prompt\n")
                # Indent with blockquote
                attacker_text = entry['attacker_prompt'].replace('\n', '\n> ')
                f.write(f"> {attacker_text}\n\n")
                
                f.write(f"#### 🔴 Target Response\n")
                target_text = entry['target_response'].replace('\n', '\n> ')
                f.write(f"> {target_text}\n\n")
            else:
                # Old Generic Schema
                role = entry.get("model_role", "Unknown Role")
                content = entry.get("content", "").replace('\n', '\n> ')
                icon = "🔴" if role == "Target" else "🔵"
                refusal_mark = " [REFUSAL DETECTED]" if refusal else ""
                
                f.write(f"### {icon} Turn {turn}: {role}{refusal_mark}\n")
                f.write(f"**Latency:** {latency:.2f} ms\n\n")
                f.write(f"> {content}\n\n")
            
            f.write("<br>\n\n---\n\n")
            
    print(f"Successfully converted {json_file} to {output_file}")

if __name__ == "__main__":
    convert_to_markdown()
