import os
import re
import random

MEMORY_FILE = "data.txt"
VERB_FILE = "verb.txt"

# PRETRAINED LANGUAGE CORE

known_verbs = {
    "is",
    "are",
    "was",
    "were",
    "have",
    "has",
    "had",
}
action_verbs = {
    "run",
    "walk",
    "eat",
    "learn",
    "know",
    "do",
    "ask",
    "asked",
    "want",
    "wanted",
    "need",
    "needed"
}
known_conjunctions = {
    "and",
    "or",
    "because",
    "but",
    "if",
    "then",
    "to",
    "of",
    "for",
    "with",
    "about"
}

known_articles = {
    "a",
    "an",
    "the"
}

known_pronouns = {
    "it",
    "they",
    "he",
    "she",
    "them",
    "you",
    "their",
    "her",
    "him",
    "his",
    "its",
}

known_adjectives = {
    "grey",
    "big",
    "small",
    "long",
    "white",
    "only",
    "national",
    "private",
    "govermental",
    "blue",
    "red",
    "black",
    "yellow",
    "green",
    "violet",
    "brown",
    "pink",
}

blocked_words = {
    "wtf",
    "lmao",
    "bruh",
    "fuck",
    "shit",
    "bitch",
    "damn",
    "asshole",
    "son of a bitch",
    "fuck off",
}

known_words = (
    known_verbs |
    known_conjunctions |
    known_articles |
    known_pronouns |
    known_adjectives
)

# GREETING ENGINE

greetings = {
    "hi",
    "hello",
    "hey",
}

# Morning greeting

morning = {
    "good morning",
    "good morrow",
}

# Health greeting

healthy = {
    "how are you?",
    "what's up?",
    "are you fine?",
    "how are you doing?",
    "are you doing well?",
}

# Noon greeting

noon = {
    "good afternoon",
    "good noon",
}

# Night greeting

night = {
    "good night",
}

# Bye(exit)

bye = {
    "bye", "goodbye",
    "have a nice day", 
}


# QUESTION ENGINE

question_words = {
    "what",
    "who",
    "why",
    "when",
    "where",
    "how",
    "whom",
    "whose",
    "define",
    "defination"
}

# ARITHMETIC ENGINE

operation_words = {
    "plus": "+",
    "add": "+",
    "added": "+",
    "addition": "+",
    "sum": "+",

    "minus": "-",
    "subtract": "-",
    "subtracted": "-",

    "times": "*",
    "multiply": "*",
    "multiplied": "*",

    "divide": "/",
    "divided": "/",

    "modulus": "%",
    "mod": "%",

    "power": "**",
    "raised": "**"
}

# MEMORY

def ensure_memory_file():

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            f.write("")

def load_memory():

    ensure_memory_file()

    memory = {}

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("[ENTITY]")

    for block in blocks:

        lines = block.strip().split("\n")

        entity = {}

        for line in lines:

            if "=" in line:

                key, value = line.split("=", 1)

                entity[key.strip()] = value.strip()

        if "name" in entity:

            memory[entity["name"].lower()] = entity

        if "types" in entity:
            entity["types"] = entity["types"].split("|")

    return memory

def rewrite_memory(memory):

    temp_file = MEMORY_FILE + ".tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as f:

        for entity in memory.values():

            f.write("\n[ENTITY]\n")

            for key, value in entity.items():

                if isinstance(value, list):
                    value = "|".join(value)

                f.write(
                    f"{key}={value}\n"
                )

    os.replace(
        temp_file,
        MEMORY_FILE
    )
def save_entity(entity):

    memory = load_memory()

    name = entity["name"].lower()

    blocked_entities = {
        "fuck",
        "shit",
        "bitch",
        "asshole",
        "wtf",
        "lmao",
        "bruh",
        "damn",
        "son of a bitch",
        "fuck off",
    }

    if name in blocked_entities:
        return

    memory[name] = entity

    rewrite_memory(memory)

#VERB
def load_actions():

    if not os.path.exists(VERB_FILE):
        open(VERB_FILE, "w").close()

    actions = []

    with open(VERB_FILE, "r", encoding="utf-8") as f:

        for line in f:

            parts = line.strip().split("|")

            if len(parts) == 3:

                actions.append({
                    "subject": parts[0],
                    "verb": parts[1],
                    "object": parts[2]
                })

    return actions

def save_action(subject, verb, obj):

    with open(VERB_FILE, "a", encoding="utf-8") as f:

        f.write(
            f"{subject}|{verb}|{obj}\n"
        )

# TOKENIZER

def tokenize(text):

    text = re.sub(
        r"[^a-zA-Z0-9\s\+\-\*\/\%\=\.\$]",
        "",
        text
    )

    return text.split()

# MORPHOLOGY

irregular_plurals = {
    "children": "child",
    "men": "man",
    "women": "woman",
    "mice": "mouse",
    "geese": "goose"
}

singular_to_plural = {
    "child": "children",
    "man": "men",
    "woman": "women",
    "mouse": "mice",
    "goose": "geese"
}

def singular_form(word):

    word = word.lower()

    if word in irregular_plurals:
        return irregular_plurals[word]

    if word.endswith("ies"):
        return word[:-3] + "y"

    if word.endswith("ves"):
        return word[:-3] + "f"

    if word.endswith("oes"):
        return word[:-2]

    if word.endswith("es"):
        return word[:-2]

    if word.endswith("s") and len(word) > 3:
        return word[:-1]

    return word

def infer_plural(word):

    return singular_form(word) != word

# INPUT CLASSIFICATION

def is_question(text):

    text = text.lower().strip()

    if text == "":
        return False

    if text.endswith("?"):
        return True

    words = text.split()

    if len(words) == 0:
        return False

    return words[0] in question_words

def is_greeting(text):

    text = text.lower().strip()

    return text in greetings

def is_morning(text):

    text = text.lower().strip()

    return text in morning

def is_noon(text):

    text = text.lower().strip()

    return text in noon

def is_night(text):
    text = text.lower().strip()

    return text in night

def is_healthy(text):
    text = text.lower().strip()

    return text in healthy

def is_bye(text):
    text = text.lower().strip()

    return text in bye

def is_arithmetic(text):

    if re.search(r"[0-9]+\s*[\+\-\*/%]\s*[0-9]+", text):
        return True

    for word in operation_words:

        if word in text.lower():
            return True

    return False

# ARITHMETIC

def extract_math_expression(text):

    text = text.lower()

    for word, symbol in operation_words.items():
        text = text.replace(word, f" {symbol} ")

    allowed = "0123456789+-*/%.() "

    cleaned = ""

    for char in text:

        if char in allowed:
            cleaned += char

    return cleaned.strip()

def solve_arithmetic(text):

    expression = extract_math_expression(text)

    if expression == "":
        return None

    try:

        allowed_chars = "0123456789+-*/%.() "

        for char in expression:

            if char not in allowed_chars:
                return None

        result = eval(
            expression,
            {"__builtins__": None},
            {}
            )

        return str(result)

    except:
        return None

# WORD ANALYSIS

def analyze_words(words, memory):

    unknown = []

    for word in words:

        lower = (
            word.lower()
            .replace(".", "")
            .replace(",", "")
            .replace("?", "")
            .replace("!", "")
            )

        singular = singular_form(lower)

        if lower in blocked_words:
            continue

        if lower in known_words:
            continue

        if lower in operation_words:
            continue

        if lower.isdigit():
            continue

        if re.fullmatch(r"[0-9+\-*/%=.$]+", lower):
            continue

        if (
            lower not in memory and
            singular not in memory
        ):
            unknown.append(word)

    return unknown

# LEARNING UNKNOWN ENTITY

def learn_entity(word, memory):

    singular = singular_form(word.lower())

    print(f"\nI do not know '{word}'.")
    print("Please teach me about it.")

    entity_type = input(
        "What type is it? (animal/object/concept/parts of speech/etc.): "
    )

    description = input("Describe it briefly: ")

    if infer_plural(word.lower()):
        a = 0
        plural = word.lower()
    else:

        a = 0

        if len(word) > 1 and word.endswith('y') and word[-2] not in 'aeiou': # y = ies
            plural = word.lower()[:-1] + "ies"

        elif word.endswith("f"): # f = ves
            plural = word.lower()[:-1] + "ves"

        elif word.endswith("o"): # o = oes
            plural = word.lower()[:-1] + "oes"

        elif word.endswith(('s', 'x', 'z', 'ch', 'sh')): 
            plural = word.lower()[:] + "es"

        elif word.endswith("lens"):
            plural = word.lower() + "es"

        elif word.lower() in singular_to_plural:
            plural = singular_to_plural[word.lower()]
    
        elif word.endswith("s") and len(word) > 3:
            plural = word.lower()[:-1]
        else:
            a = 1

    if a == 1:
        entity = {
            "name": singular,
            "type": entity_type,
            "description": description
            }
    else:
        entity = {
            "name": singular,
            "plural": plural,
            "type": entity_type,
            "description": description
            }

    save_entity(entity)

    memory[singular] = entity

    print(f"\nThanks for teaching me this: {singular}")

# ATTRIBUTE EXTRACTION

attribute_patterns = [
    "colour",
    "color",
    "size",
    "weight",
    "height"
]

def extract_attributes(subject, sentence, entity):

    lower = sentence.lower()

    colors = [
        "red",
        "blue",
        "green",
        "grey",
        "gray",
        "black",
        "white",
        "yellow",
        "brown"
    ]

    for color in colors:

        if color in lower:
            entity["color"] = color

# RELATIONSHIP LEARNING

def learn_statement(sentence, memory):

    words = tokenize(sentence)

    lower_words = [w.lower() for w in words]

    articles = {"a",
                "an",
                "the"
                }

    linking_verbs = {"is",
                     "are",
                     "was",
                     "were",
                     "am",
                     "have",
                     "has",
                     "had"
                     }
    subject = None
    verb = None
    verb_index = -1

    for i, word in enumerate(lower_words):

        if word in action_verbs:
            verb = word
            verb_index = i
            break

    if verb is not None:

        for i in range(verb_index):

            if lower_words[i] not in articles:
                subject = singular_form(lower_words[i])
                break

        if subject:

            obj = " ".join(words[verb_index + 1:])

            save_action(
                subject,
                verb,
                obj
                )

            print("\nI learned verb:")
            print(f"{subject} {verb} {obj}")

            return True
        
    for verb in linking_verbs:

        if verb in lower_words:

            index = lower_words.index(verb)

            if index > 0 and index < len(words) - 1:

                subject = words[index - 1].lower()

                if verb in {"are", "were", "have"}:
                    subject = singular_form(subject)

                predicate_words = []

                for w in words[index + 1:]:

                    if "." in w or "!" in w or "?" in w:

                        cleaned_word = (
                            w.replace(".", "")
                             .replace("!", "")
                             .replace("?", "")
                        )

                        if cleaned_word != "":
                            predicate_words.append(cleaned_word)

                        break

                    predicate_words.append(w)

                predicate_words = [
                    w for w in predicate_words
                    if w.lower() not in articles
                ]



                cleaned = []

                for w in predicate_words:

                    clean_word = (
                        w.replace(".", "")
                         .replace(",", "")
                         .replace("?", "")
                         .replace("!", "")
                    )

                    cleaned.append(clean_word)


                    if len(cleaned) > 0:

                        cleaned[-1] = singular_form(cleaned[-1])


                predicate = " ".join(cleaned).lower()

# CONTRADICTION DETECTION
                if subject in memory:

                    existing_types = memory[subject].get(
                        "types",
                        [memory[subject]["type"]] if "type" in memory[subject] else []
                        )

                    if predicate not in existing_types:
                        temp_types = existing_types.copy()
                        temp_types.append(predicate)

                        print(f"\nI think you earlier said that:")
                        print(f"{subject} is: {temp_types}")
                        print(f"This is what you told now:")
                        print(f"{subject} is: {predicate}")

                        choice = input(
                            "Should I replace the old one with this\nYes or No: "
                        ).lower()

                        if choice != "yes":
                            return True
                        existing_types = memory[subject].get(
                            "types",
                            [memory[subject]["type"]] if "type" in memory[subject] else []
                            )
                    if predicate not in existing_types:
                        existing_types.append(predicate)

                if subject in memory:
                    entity = memory[subject]
                    existing_types = entity.get("types", [])

                    if predicate not in existing_types:
                        existing_types.append(predicate)
                        entity["types"] = existing_types
                else:
                    entity = {
                        "name": subject,
                        "types": [predicate],
                        "description": sentence
                        }
                
                if verb == "are":
                    entity["plural"] = words[index - 1].lower()

                extract_attributes(subject, sentence, entity)

                save_entity(entity)

                memory[subject] = entity

                print(f"\nI learned this:")
                print(f"{subject} -> {predicate}")

                return True

    return False

# KNOWLEDGE CHAINING

def build_knowledge_chain(
    entity_name,
    memory,
    max_depth=5
):

    visited = set()

    chain = []

    current = entity_name.lower()

    depth = 0
    while (
        current in memory and
        current not in visited and
        depth < max_depth
        ):

        visited.add(current)

        entity = memory[current]

        types = entity.get("types")

        if types is None:

            if "type" in entity:
                types = [entity["type"]]
            else:
                break

        if len(types) == 0:
            break

        type_name = ", ".join(types)

        article = "a"

        if type_name[0].lower() in ["a", "e", "i", "o", "u"]:
            article = "an"

        sentence = (
            f"{entity['name'].capitalize()} "
            f"is {article} {type_name}."
        )

        # attributes
        if "color" in entity:
            sentence += f" It is {entity['color']}."

        chain.append(sentence)

        depth += 1

        current = singular_form(type_name.split()[0])

    return " ".join(chain)


# REVERSE RELATIONSHIP LOOKUP
def normalize_description(text):
    """Normalize a description so it can be matched in either direction."""
    text = re.sub(r"[^a-zA-Z0-9\s'-]", "", text).lower().strip()
    words = text.split()
    while words and words[0] in {"a", "an", "the"}:
        words.pop(0)
    return " ".join(words)


def find_entity_by_description(question, memory):
    """
    Answer questions such as 'Who is a good boy?' by searching
    the descriptions/types already stored for each entity.
    """
    match = re.match(
        r"^\s*who\s+(?:is|are|was|were)\s+(.+?)\s*\??\s*$",
        question,
        flags=re.IGNORECASE
    )
    if not match:
        return None

    wanted = normalize_description(match.group(1))
    if not wanted:
        return None

    matches = []
    for entity in memory.values():
        descriptions = entity.get("types", [])
        if isinstance(descriptions, str):
            descriptions = descriptions.split("|")
        if not descriptions and entity.get("type"):
            descriptions = [entity["type"]]

        for description in descriptions:
            if normalize_description(description) == wanted:
                matches.append(entity.get("name", "").capitalize())
                break

    if matches:
        return ", ".join(matches) + "."
    return None

# RESPONSE ENGINE

def answer_question(user_input, memory):

    actions = load_actions()

    lower = user_input.lower()

    # Reverse lookup must run before ordinary entity lookup.
    # Example: "Who is a good boy?" -> "Ratin."
    reverse_answer = find_entity_by_description(user_input, memory)
    if reverse_answer:
        return reverse_answer

    arithmetic_result = solve_arithmetic(lower)

    if arithmetic_result:
        return arithmetic_result

    words = tokenize(lower)

    for word in words:

        singular = singular_form(word)

        if singular in memory:

            return build_knowledge_chain(
                singular,
                memory,
                max_depth=5
                )

    if is_greeting(lower):
        return random.choice([
        "Hello", "Hi", "Hey"
    ])
    if is_healthy(lower):
        return random.choice([
            "I am fine. Thanks for asking.",
            "I am doing well. Thank you for asking.",
            ])
    if is_morning(lower):
        return "Good Morning."
    
    if is_noon(lower):
        return "Good Afternoon."
    
    if is_night(lower):
        return "Good Night."

    
    if is_bye(lower):
        return "Bye.\nShutting down."

    for word in words:
        subject = singular_form(word)
        related = []

        for action in actions:
            if action["subject"] == subject:
                related.append(
                    f"{subject} {action['verb']} {action['object']}"
                    )
                if related:
                    return ". ".join(related)

    memory = load_memory()
    return random.choice([
        "I do not know that yet. Teach me",
        "I need information about this. If you know it, then please teach me"
    ])

# MAIN LOOP

def main():

    print("-" * 50)
    print(" Cognitive AI Engine")
    print("_" * 50)

    memory = load_memory()

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:

            print("Shutting down.")

            break

        memory = load_memory()

        # greeting
        if is_greeting(user_input):

            response = answer_question(user_input, memory)

            print(f"\nAI: {response}")

            continue

        # morning
        if is_morning(user_input):

            response = answer_question(user_input, memory)

            print(f"\nAI: {response}")

            continue
        
        # noon
        if is_noon(user_input):

            response = answer_question(user_input, memory)

            print(f"\nAI: {response}")

            continue
          
        # night
        if is_night(user_input):

            response = answer_question(user_input, memory)

            print(f"\nAI: {response}")

            continue

        # bye
        if is_bye(user_input):

            response = answer_question(user_input, memory)

            print(f"\nAI: {response}")

            break

        memory = load_memory()
  
        # arithmetic
        if is_arithmetic(user_input):

            response = solve_arithmetic(user_input)

            if response:

                print(f"\nAI: {response}")

                continue

        # question
        if is_question(user_input):

            response = answer_question(user_input, memory)

            print(f"\nAI: {response}")

            continue

        # learning statement
        learned = learn_statement(user_input, memory)

        if learned:

            print("\nAI: Thanks for teaching . I learned it.")

            continue

        # unknown learning
        words = tokenize(user_input)

        unknown_words = analyze_words(words, memory)

        learned_anything = False

        for word in unknown_words:

            if len(word) > 2:

                learn_entity(word, memory)

                learned_anything = True

        if learned_anything:

            print("\nAI: Thanks for teaching. I learned it.")

if __name__ == "__main__":
    main()
