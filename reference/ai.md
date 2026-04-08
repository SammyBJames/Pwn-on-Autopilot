# AI for Scripting

LLMs are incredible at speeding up scripting and generating code. They remove the friction of remembering syntax and let you focus on the logic of your attack. 

Here are my recommendations for how to use AI effectively when writing hacking scripts:

## Verify Everything!
**Never blindly run code you have not thoroughly reviewed.** 

If you ask an AI to fix a script, parse a payload, or analyze a vulnerability, you must read the output carefully before executing it. 
1. **Hallucinations:** AI will often invent things that don't exist or are outdated, making your scripts very unreliable.
2. **Security Risk:** If you paste code from the Internet, you very well might get prompt-injected.

Treat the AI like a dumb intern. It can write code fast, but you must be the Senior Engineer reviewing the output. If you let it go without supervision, it will bring down the entire company.

## Generate Boilerplate & Scaffold
Never start from an empty file. AI is exceptionally good at writing the repetitive scaffolding required for your script.

You jump straight into the actual logic of the exploit within 10 seconds, instead of spending 5 minutes writing `parser.add_argument()` line-by-line. Describe *how* the script should work, and let your LLM set up the project structure.

Break the problem down into smaller steps and have the AI generate step-by-step. You can then make sure that the model is staying on track and not introducing bugs or other issues. LLMs are much more effective when they focus on one small task at a time.

**Example Prompt:**
> "Let's write a Python script using `argparse` and `requests`. It will accept a target URL and an optional wordlist file, then send a GET request for every word using a Session object with a timeout of 5 seconds. Start by creating the argument parser and setting up the Session with retries."


## Parsing
Writing regular expressions or parsing data manually is a waste of time now. Give the LLM a sample of the data and have it write the parser for you. Whether it's HTML, JSON, or something interesting, AI can extract exactly what you need quick.

**Example Prompt:**
> "Here is a chunk of HTML from a target site: `[HTML]`. Write a function that extracts the value of the anti-CSRF token hidden inside the third div using BeautifulSoup."

## Explaining & Deobfuscating
You will often encounter problems where there is some (intended or not) "security through obscurity". Especially when working with binary data, it is often hard to decipher exactly what you're looking at. Have your LLM rewrite the data in a more human-readable format, and explain how it works. Being able to reverse-engineer in minutes rather than hours is game changing (literally for CTFs). Limit tooling so you don't get injected!

**Example Prompt:**
> "I have this JPG file I am analyzing. Can you help me determine what type of JPG this is and where the Start of Frame (SOF) marker is? Here is the hex dump: `[hex]`."

## Refactoring
Most beginner hacking scripts are simple and often unoptimal. They work, but not as well as they could. Give an LLM the working prototype and have it refactor the slowest parts to be more efficient. For certain tasks, speed is critical (race conditions?).

**Example Prompt:**
> "I have this Python script that checks if a list of directories exists. I want to make it faster by using multithreading. Can you refactor the code to run in parallel rather than sequentially?"

## Debugging
When your script is crashing with an obscure error, give AI the error and your project context and it will usually be able to tell you what the issue is after a try or two. Even if it can't fix it itself, it can usually decipher the cryptic error message and point you in the right direction.

Be careful when debugging with AI because it can often get off track and go down a rabbit hole. Use your knowledge and intuition to steer it in the right direction and cut it off before it goes too far.

**Example Prompt:**
> "My pwntools script is crashing with 'EOFError' immediately after I send the payload. Here is my code: `[paste code]`."
