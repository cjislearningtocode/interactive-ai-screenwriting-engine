import os
import sys
import json
import time
import datetime
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_screenwriting_ideas(user_genre, skill_level, focuses_on_block=False):
    """
    Formulates a structured prompt and calls Gemini to get high-concept loglines and a brief breakdown of 'what it's about'.
    """
    block_context = "The writer is currently experiencing writer's block, so give them extra jarring, unexpected inciting incidents." if focuses_on_block else ""
    
    prompt = f"""
    You are an expert Hollywood development executive and screenwriting mentor.
    The user is a {skill_level}-level screenwriter who loves the '{user_genre}' genre. {block_context}

    Generate 3 unique, high-concept movie or series ideas for a {story_format}. For each idea, provide:
    1. A bold TITLE.
    2. A compelling, one-sentence LOGLINE (focusing on protagonist, inciting incident, goal, and stakes).
    3. A short paragraph ("What it's about") detailing the central conflict, tone, and the core journey.

    Keep the ideas fresh, original, and deeply engaging. Format clearly with clean spacing for a terminal screen.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def flesh_out_idea(title, genre, story_format, logline=""):
    """
    Takes a selected idea title and its logline, expanding it into a detailed blueprint.
    """
    prompt = f"""
    You are an expert story editor and narrative consultant. The user selected this concept to develop into a {story_format}:
    TITLE: {title}
    GENRE: {genre}
    LOGLINE/PREMISE: {logline}

    STRICT RULE: You must base the breakdown completely on the provided LOGLINE/PREMISE. Do not invent a completely different concept or setting. Expand exactly on what is written.

    Provide a detailed breakdown including:
    1. Three-Act Structure outline (Act 1, Act 2a, Act 2b, Act 3) scaled perfectly for a {story_format}
    2. Main character arcs for the protagonist and antagonist
    3. Key turning points and their emotional impact
    """
        
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def save_ideas_to_file(name, genre, ideas, prefix="PITCHES", story_format="Feature-Length Movie", logline=""):
    """Saves the generated AI ideas and session metadata into a structured JSON file."""
    now = datetime.datetime.now()
    timestamp_log = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = now.strftime("%Y-%m-%d_%H-%M")
    
    safe_genre = genre.replace(" ", "_") if genre else "general"
    folder_name = "saved_pitches"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created a new folder: '{folder_name}'")
        
    filename = f"{folder_name}/{prefix}_{timestamp_file}_{safe_genre}.json"
    
    session_data = {
        "metadata": {
            "screenwriter": name,
            "generated_on": timestamp_log,
            "genre": genre,
            "story_format": story_format,
            "prefix": prefix
        },
        "logline": logline,
        "content": ideas
    }
    
    with open(filename, "w") as file:
        json.dump(session_data, file, indent=4)
        
    print(f"File saved successfully as: '{filename}'")
    return filename


def load_project_file():
    """Scans the saved_pitches directory and lets the user pick a past session."""
    folder_name = "saved_pitches"
    if not os.path.exists(folder_name) or not os.listdir(folder_name):
        print("\n[!] No saved project files found.")
        return None
        
    files = [f for f in os.listdir(folder_name) if f.endswith('.json')]
    if not files:
        print("\nNo saved JSON projects found.")
        return None
        
    print("\n--- SELECT A PREVIOUS SESSION ---")
    for idx, f in enumerate(files, 1):
        print(f"{idx}. {f}")
        
    try:
        choice = int(input(f"Select a file (1-{len(files)}): "))
        selected_file = os.path.join(folder_name, files[choice - 1])
        with open(selected_file, "r") as file:
            return json.load(file)
    except (ValueError, IndexError):
        print("[!] Invalid selection.")
        return None

print("                         *** ANOTHER ONE THEN AGAIN ***                          ")
print("                         Your AI Screenwriting Helper.                           ")

chosen_genre = ""
ideas = ""

while True:
    print("\n==============================================")
    print("1. Start a Brand New Script Project")
    print("2. Load a Previous Project / Blueprint")
    print("3. Exit")
    init_choice = input("Select an option (1-3): ").strip()
    
    if init_choice == "3":
        print("Happy writing!")
        break
        
    name = ""
    story_format = "Creative Project"
    chosen_genre = ""
    ideas = ""
    target_title = ""
    target_logline = ""
    goto_flesh_out = False
    
    if init_choice == "2":
        project = load_project_file()
        if not project:
            continue 
            
        name = project["metadata"]["screenwriter"]
        chosen_genre = project["metadata"]["genre"]
        story_format = project["metadata"]["story_format"]
        ideas = project["content"]
        target_logline = project.get("logline", "")
        
        print(f"\nWelcome back, {name}!")
        print(f"Loaded Workspace: {story_format} | Genre: {chosen_genre.upper()}")
        
        if project["metadata"]["prefix"] == "FLESHED_OUT":
            target_title = input("Confirm the TITLE of the project you are working on: ").strip()
            mode_choice = "2" 
        else:
            print("\nHere are your saved pitches:")
            print(ideas)
        
        goto_flesh_out = True

    else:
        name= input("Please enter your name: ")
    print(f"Hello {name}.")
    print("\nWhat format are you looking to create today?")
    print("1. Feature-Length Movie")
    print("2. Serialized TV Series / Pilot")
    print("3. Stage Play")
    print("4. Short Film")
    format_choice = input("Select a number (1-4) or type your custom format (e.g., Novel, Comic Book): ")
    if format_choice == "1":
        story_format = "Feature-Length Movie"
    elif format_choice == "2":
        story_format = "Serialized TV Series / Pilot"
    elif format_choice == "3":
        story_format = "Stage Play"
    elif format_choice == "4":
        story_format = "Short Film"
    else:
        story_format = format_choice if format_choice else "Creative Project"

    scale=int(input("On a scale of 1-10, where do you rank yourself as a screenwriter (1 being beginner and 10 being pro): "))
    if scale<=3:
        print("Okay. Do you think that you know the basics?")
        basics=input("Yes or no?: ").lower()
        if basics == 'yes' or basics =='y':
            print("And how often do you think you write?")
            often_write=int(input("Enter in days: "))
            print("What genre(s) do you often gravitate to?")
            chosen_genre= input("Please list them with no commas but just a space:").lower()
            print("\n Generating beginner-friendly loglines...")
            ideas = get_screenwriting_ideas(chosen_genre, "beginner", story_format)
            print("\n" + ideas)
        elif basics=='no' or basics=='n':
            print("We'll start from scratch. What genre do you like to watch?")
            chosen_genre=input("Enter them without commas just with a space:").lower()
            print("\nGenerating foundational concept pitches based on what you watch...")
            ideas = get_screenwriting_ideas(chosen_genre, "absolute beginner", story_format)
            print("\n" + ideas)
    elif 3<scale<=6:
        print("I would consider you an intermediate. On a scale of the most popular movie/show you know to what you write, rate using 1-3 how good you are.")
        good_rate= int(input("Enter using 1-3:"))
        if good_rate<=3:
            print("Okay a beginner intermediate.")
            chosen_genre=input("Enter what genre you like to watch/write. No commas please just a space:").lower()
            print("\nFetching intermediate concept ideas...")
            ideas = get_screenwriting_ideas(chosen_genre, "beginner-intermediate", story_format)
            print("\n" + ideas)
    elif scale>6:
        print("We've got a pro on our hands.")
        scripts_total=int(input("Tell me how many scripts have you written:"))
        if scripts_total>=1:
            print("Do you have writer's block?")
            writers_block= input("Yes or no:").lower()
            chosen_genre = input("What specific genre or hybrid genre are we executing?: ").strip()
            if writers_block=='yes' or writers_block=='y':
                how_often=int(input("How often. Input number of times you would say you get writers' block:"))
                print(f"\nBlasting through writer's block with some heavy-hitting concepts {story_format}...")
                ideas = get_screenwriting_ideas(chosen_genre, "professional", focuses_on_block=True)
                print("\n" + ideas)
            else:
                print(f"\nGenerating fresh pro-tier {story_format} concepts...")
                ideas = get_screenwriting_ideas(chosen_genre, "professional")
                print("\n" + ideas)
   
    if not ideas:
       
        print(f"\nGenerating pro {story_format} concepts...")
        ideas = get_screenwriting_ideas(chosen_genre or "general", "professional", story_format)
        print("\n" + ideas)

    goto_flesh_out = True

    if goto_flesh_out:
            if init_choice != "2":
                save_choice = input("Would you like to save these ideas to a file? (yes/no): ").strip().lower()
                if save_choice in ["yes", "y"]:
                    save_ideas_to_file(name, chosen_genre or "general", ideas, prefix="PITCHES", story_format=story_format)
            
            if 'mode_choice' not in locals() or mode_choice != "2":
                flesh_it_out = input("\nDo you want to deeply flesh out one of these ideas right now? (yes/no): ").strip().lower()
                
                if flesh_it_out in ["yes", "y"]:
                    target_input = input("Type the number (1-3) or paste the exact TITLE of the idea: ").strip()
                    target_title = target_input
                    
                    if target_input in ["1", "2", "3"]:
                        print(f"Searching your pitches for Idea #{target_input}...")
                        lines = ideas.split("\n")
                        target_logline = ""
                        
                        for i, line in enumerate(lines):
                            if f"{target_input}." in line or f"*{target_input}." in line or f"IDEA {target_input}" in line:
                                for sub_line in lines[i:i+6]:
                                    if "TITLE:" in sub_line.upper():
                                        target_title = sub_line.upper().replace("TITLE:", "").replace("**", "").replace("#", "").strip()
                                    if "LOGLINE:" in sub_line.upper():
                                        target_logline = sub_line.replace("LOGLINE:", "").replace("**", "").replace("*", "").strip()
                                break
                        
                        if target_title != target_input:
                            print(f"Auto-detected Title: '{target_title}'")
                        else:
                            print("Could not parse title automatically. Defaulting to input selection.")
                    
                    print(f"\n--- WHAT ARE WE DEVELOPING FOR '{target_title}'? ---")
                    print("1. Generate a structural script blueprint")
                    print("2. Paste / Type a rough scene layout to polish for subtext")
                    mode_choice = input("Select an option (1-2): ").strip()
                else:
                    mode_choice = ""
            
            if mode_choice == "1":
                detailed_blueprint = flesh_out_idea(target_title, chosen_genre or "general", story_format, target_logline)
                print("\n" + detailed_blueprint)
                
                save_ideas_to_file(name, chosen_genre or "general", detailed_blueprint, prefix="FLESHED_OUT", story_format=story_format, logline=target_logline)
                print("\nWork compiled successfully. Happy writing!")
                
            elif mode_choice == "2":
                print(f"\nPaste your rough script layout or scene drafts for '{target_title}' below.")
                print("When you are entirely finished pasting, press ENTER ON A BLANK LINE to run the tool.")
                print("-" * 60)
                
                scene_lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    scene_lines.append(line)
                    
                user_scene = "\n".join(scene_lines)
                
                if user_scene.strip():
                    print(f"\nTransforming scene pages... refining formatting metrics...")
                    
                    refine_prompt = f"""
    You are an elite Hollywood screenplay doctor. Take this raw scene layout written for the project '{target_title}' ({story_format} / Genre: {chosen_genre}).
    Original Context: {target_logline}

    Rewrite it to conform to professional cinematic pacing:
    1. Inject heavy subtext—characters shouldn't say exactly what they mean.
    2. Keep descriptive action paragraphs punchy and under 3 lines.

    RAW PAGES:\n{user_scene}
    """
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=refine_prompt,
                    )
                    
                    print("\n" + "="*20 + " POLISHED CINEMATIC SCENE " + "="*20)
                    print(response.text)
                    print("="*66)
                    
                    save_ideas_to_file(name, chosen_genre or "general", response.text, prefix="SUBTEXT_PASS", story_format=story_format, logline=target_logline)
                else:
                    print("No text detected.")
                    
                print("\nWork compiled successfully. Happy writing!")
 
            if 'mode_choice' in locals():
                del mode_choice
    break