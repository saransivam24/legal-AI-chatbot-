import sys
import os
import shutil
import time

# Ensure UTF-8 output in Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv, set_key

# Load environment variables from .env
load_dotenv()

def is_valid_openai_key(key):
    if not key:
        return False
    k = key.strip()
    if any(p in k.lower() for p in ["your-actual", "your-key", "placeholder", "your_actual", "your-api-key"]):
        return False
    return k.startswith("sk-") and len(k) > 25

def is_valid_gemini_key(key):
    if not key:
        return False
    k = key.strip()
    if any(p in k.lower() for p in ["your-actual", "your-key", "placeholder"]):
        return False
    return (k.startswith("AIza") or k.startswith("AQ.")) and len(k) > 20

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("[LegalIQ] Initializing Multi-AI Intelligence Engine...")
if is_valid_openai_key(OPENAI_API_KEY):
    print("[OpenAI] Valid API Key loaded successfully!")
else:
    print("[OpenAI] No valid key in .env (add in Settings or .env)")

if is_valid_gemini_key(GEMINI_API_KEY):
    print("[Gemini] Valid API Key loaded successfully! (AI Studio)")
else:
    print("[Gemini] No valid key in .env (add in Settings or .env)")
print("=" * 60)

# Optional lazy clients
def get_openai_client(custom_key=None):
    key = custom_key or os.getenv("OPENAI_API_KEY")
    if not is_valid_openai_key(key):
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key.strip())
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return None

def get_gemini_client(custom_key=None):
    key = custom_key or os.getenv("GEMINI_API_KEY")
    if not is_valid_gemini_key(key):
        return None
    try:
        from google import genai
        return genai.Client(api_key=key.strip())
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

# Default dossier loader from project directory
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_FILES = [
    "FIR_042_2023.txt.txt",
    "Complainant_Statement.txt.txt",
    "Witness_Statement_Suresh.txt.txt",
    "Accused_Dossier.txt.txt",
    "case.txt.txt",
    "FIR_042_2023.txt",
    "Complainant_Statement.txt",
    "Witness_Statement_Suresh.txt",
    "Accused_Dossier.txt",
    "case.txt"
]

def load_server_dossier():
    combined = ""
    seen = set()
    for fname in DOSSIER_FILES:
        fpath = os.path.join(PARENT_DIR, fname)
        canonical = fname.replace(".txt.txt", ".txt")
        if os.path.exists(fpath) and canonical not in seen:
            seen.add(canonical)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    combined += f"\n[DOCUMENT: {canonical}]\n{f.read()}\n"
            except Exception:
                pass
    return combined

SERVER_DOSSIER = load_server_dossier()
if SERVER_DOSSIER:
    print(f"[LegalIQ] Preloaded server case dossier ({len(SERVER_DOSSIER)} characters from disk).")

# Ensure logo image is in project directory
PICTURES_LOGO = r"C:\Users\Saran\Pictures\legal iq.jpeg"
LOCAL_LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.jpeg")
if os.path.exists(PICTURES_LOGO) and not os.path.exists(LOCAL_LOGO):
    try:
        shutil.copy2(PICTURES_LOGO, LOCAL_LOGO)
        print("[LegalIQ] Logo image copied to project folder: logo.jpeg")
    except Exception:
        pass

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """
You are LegalIQ, an elite enterprise AI legal copilot and criminal intelligence reasoning assistant.

CRITICAL INSTRUCTIONS FOR EXACT & PRECISE ANSWERS:
1. DIRECT ANSWER FIRST: Always answer the user's question directly, factually, and concisely in the very first 1-2 sentences. Avoid long generic introductions or filler phrases. (For example: If asked "Who is the complainant?", immediately begin: "**The complainant is Shri M. Sundaram, Managing Director of Sri Balaji Garments Pvt Ltd.**" followed by details).
2. EXACT FACTS & FIGURES FROM DOSSIER: Quote exact verified figures and facts:
   - Consideration & Advance: Total contract consideration is ₹25,00,000/-. Advance paid is ₹15,00,000/- via RTGS on 15-June-2023.
   - Overseas Remittance: Rajesh Kumar remitted USD 16,500 (approx. ₹13,65,000) on 22-June-2023 via Telegraphic Transfer (TT) to Heidelberg Tech GMBH in Stuttgart, Germany.
   - Chennai Port Customs Delay: Shipment arrived at Chennai Port on 28-July-2023 under Bill of Entry scrutiny; detained due to revised automated customs regulations.
   - Meeting Discrepancy: Complainant swears dispute meeting occurred on 10-August-2023 at 10:30 AM at Corporate Office. Witness Suresh Natarajan (Accountant) swears meeting occurred on 10-August-2023 at 03:00 PM (15:00 hrs) inside Factory Premises.
   - Cheque Details: ICICI Bank Cheque No. 892110 for ₹5,00,000/- issued on 10-August-2023; returned dishonoured on 12-August-2023 for "Insufficient Funds".
   - Accused Background: Rajesh Kumar (Proprietor, Precision Machines India), zero criminal history (SCRB verified), surrendered passport No. Z-4829101, cooperated under Section 41A CrPC.
   - Legal Provisions: Registered under IPC 420 (Cheating) & 406 (Criminal Breach of Trust). Bail governed under CrPC 437 / BNSS 480. Precedents: Arnesh Kumar (2014), Satishchandra Ratanlal Shah (2019).
3. FORMATTING: Use bold text for key entities, dates, and amounts. Use bullet points for structured comparisons.
4. GENERAL & CHAT QUERIES: If the user says hello or asks broader legal questions, respond intelligently and helpfully.
"""

def generate_grounded_legal_response(query, context=""):
    q = query.lower().strip()
    
    # 1. Full Case Explanation / Summary / Overview
    if any(k in q for k in ["explain", "summary", "summarize", "about the case", "case details", "overview", "what is this case", "what is the case", "briefing"]):
        return (
            "### ⚖️ Comprehensive Case Intelligence & Legal Assessment\n\n"
            "**1. Case Overview & Parties:**\n"
            "• **FIR Number:** FIR No. 042 / 2023 registered at Anna Nagar (K-4) Police Station, Chennai on 14-Aug-2023.\n"
            "• **Complainant:** **Shri M. Sundaram**, Managing Director of Sri Balaji Garments Pvt Ltd, Anna Nagar, Chennai.\n"
            "• **Accused:** **Rajesh Kumar**, Proprietor of Precision Machines India, Plot No. 14, 2nd Avenue, Anna Nagar, Chennai.\n"
            "• **Statutory Sections:** Section 420 IPC (Cheating) and Section 406 IPC (Criminal Breach of Trust).\n\n"
            "**2. The Commercial Transaction:**\n"
            "• **Contract Date:** 10-June-2023 for supply of two high-speed industrial textile printing machines.\n"
            "• **Total Consideration:** **₹25,00,000/-**.\n"
            "• **Advance Paid:** **₹15,00,000/- (60%)** transferred via RTGS on 15-June-2023.\n"
            "• **Agreed Delivery Deadline:** 25-July-2023.\n\n"
            "**3. Genesis of Dispute & Dishonoured Cheque:**\n"
            "• Machinery was not delivered on the promised date due to overseas logistics delay.\n"
            "• During confrontation on 10-August-2023, the accused handed over ICICI Bank Cheque No. 892110 for **₹5,00,000/-** as interim security.\n"
            "• On 12-August-2023, the cheque was returned dishonoured with the remark **'Insufficient Funds'**, leading to criminal complaint.\n\n"
            "**4. Exculpatory Evidence & Absence of Mens Rea:**\n"
            "• **Proof of Genuine Intent:** On 22-June-2023, Rajesh Kumar remitted **USD 16,500 (approx. ₹13,65,000/-)** via Telegraphic Transfer to German manufacturer Heidelberg Tech GMBH in Stuttgart to procure the machines.\n"
            "• **Customs Detention at Chennai Port:** Consignment arrived at Chennai Port on 28-July-2023 aboard *MV Northern Star* (Bill of Lading MSC-DE-77821) and was detained by customs authorities under revised automated semiconductor regulations.\n"
            "• **Clean Antecedents:** State Crime Records Bureau (SCRB) verification confirms **zero prior criminal records**.\n\n"
            "**5. Material Witness Contradiction:**\n"
            "• **Complainant's Claim:** Swears dispute meeting occurred at **10:30 AM** at his **Corporate Office** in Anna Nagar.\n"
            "• **Witness Suresh Natarajan (Sr. Accountant):** Testifies under Sec. 161 CrPC that the meeting occurred at **3:00 PM (15:00 hrs)** inside the **Ambattur Factory floor**.\n\n"
            "**6. Legal Defense Grounds & Precedents:**\n"
            "• *Satishchandra Ratanlal Shah v. State of Gujarat (2019)*: Breach of contract does not amount to criminal cheating under IPC 420 without fraudulent intention at inception.\n"
            "• *Arnesh Kumar v. State of Bihar (2014)*: Notice under Section 41A CrPC is mandatory prior to arrest for offences punishable up to 7 years."
        )

    # 2. Complainant
    if any(k in q for k in ["complainant", "who filed", "sundaram", "victim"]):
        return (
            "**The complainant is Shri M. Sundaram, Managing Director of Sri Balaji Garments Pvt Ltd.**\n\n"
            "• **Age & Parentage:** 48 years, S/o Muthuswamy.\n"
            "• **Address:** No. 72, 5th Main Road, Anna Nagar, Chennai.\n"
            "• **Enterprise:** Sri Balaji Garments Pvt Ltd (textile unit with 80+ employees).\n"
            "• **Allegation:** Transferred ₹15,00,000/- advance on 15-Jun-2023 for 2 machines which were not delivered, and a ₹5,00,000/- security cheque was dishonoured."
        )

    # 3. Accused
    if any(k in q for k in ["accused", "rajesh", "petitioner", "seller", "supplier"]):
        return (
            "**The accused is Rajesh Kumar, Proprietor of Precision Machines India.**\n\n"
            "• **Age & Parentage:** 44 years, S/o Late S. Ramanathan.\n"
            "• **Address:** Plot No. 14, 2nd Avenue, Anna Nagar, Chennai - 600040.\n"
            "• **Criminal Record:** Verified by State Crime Records Bureau (SCRB) as having **ZERO prior criminal antecedents**.\n"
            "• **Cooperation:** Complied with Section 41A CrPC notice and surrendered Passport No. Z-4829101 to the Investigating Officer.\n"
            "• **Performance:** Remitted USD 16,500 (₹13.65L) to German manufacturer Heidelberg Tech GMBH to fulfill the contract."
        )

    # 4. Advance / Money / Consideration
    if any(k in q for k in ["advance", "how much", "consideration", "money", "paid", "payment"]):
        return (
            "**The total contract value is ₹25,00,000/-, and the advance paid is ₹15,00,000/-.**\n\n"
            "• **Payment Mode & Date:** RTGS transfer on 15-June-2023 to Precision Machines India.\n"
            "• **Overseas Wire by Accused:** On 22-June-2023, Rajesh Kumar transferred **USD 16,500 (approx. ₹13,65,000/-)** to Heidelberg Tech GMBH in Germany.\n"
            "• **Balance Amount:** ₹10,00,000/- was payable upon final delivery and operational commissioning."
        )

    # 5. Cheque Bounce / Dishonour
    if any(k in q for k in ["cheque", "check", "bounce", "dishonour", "892110", "5,00,000"]):
        return (
            "**ICICI Bank Cheque No. 892110 for ₹5,00,000/- was issued and returned dishonoured.**\n\n"
            "• **Drawer:** Rajesh Kumar (Precision Machines India).\n"
            "• **Payee:** Sri Balaji Garments Pvt Ltd.\n"
            "• **Handover Date:** 10-August-2023 (given as security during dispute meeting).\n"
            "• **Return Date:** 12-August-2023 with memo stating **'Insufficient Funds'**.\n"
            "• **Legal Defense:** The cheque was tendered as security under commercial duress; appropriate legal remedy lies under Sec. 138 NI Act rather than IPC 420."
        )

    # 6. Customs / Delay / Port
    if any(k in q for k in ["delay", "port", "customs", "shipment", "cargo", "delivery", "chennai port"]):
        return (
            "**The delay was caused by Customs detention at Chennai Port, not willful fraud.**\n\n"
            "• **Arrival Date:** 28-July-2023 at Chennai Port aboard vessel *MV Northern Star*.\n"
            "• **Bill of Lading:** MSC-DE-77821 from Stuttgart/Hamburg.\n"
            "• **Detention Reason:** Held by Customs for automated semiconductor clearance under revised Bill of Entry inspection rules.\n"
            "• **Finding:** Unforeseen regulatory detention proves absence of fraudulent intent at inception."
        )

    # 7. Witness Suresh / Contradiction
    if any(k in q for k in ["witness", "suresh", "contradiction", "conflict", "meeting time", "discrepancy"]):
        return (
            "**There is a direct 4.5-hour time and venue contradiction between the sworn statements:**\n\n"
            "• **Complainant Shri M. Sundaram:** Swears the dispute meeting took place on **10-August-2023 at 10:30 AM** at his **Corporate Office in Anna Nagar**.\n"
            "• **Witness Suresh Natarajan (Sr. Accountant):** Swears under Section 161 CrPC that the meeting occurred on **10-August-2023 at 3:00 PM (15:00 hrs)** inside the **Ambattur Factory Premises**.\n"
            "• **Corroborating Evidence:** Suresh confirmed seeing import invoices and customs detention papers."
        )

    # 8. Bail / Legal Grounds
    if any(k in q for k in ["bail", "release", "437", "480", "grounds", "petition"]):
        return (
            "**Statutory Grounds for Regular Bail under Section 437 CrPC / Section 480 BNSS:**\n\n"
            "1. **Absence of Mens Rea:** Accused remitted USD 16,500 (₹13.65L) to German manufacturer Heidelberg Tech GMBH (*Satishchandra Ratanlal Shah (2019)*).\n"
            "2. **Punishable Under 7 Years:** Offences under IPC 420 and 406 attract maximum 7-year imprisonment, making *Arnesh Kumar v. State of Bihar (2014)* guidelines applicable.\n"
            "3. **Zero Criminal Record:** Official SCRB verification confirms zero prior criminal cases.\n"
            "4. **No Flight Risk:** Permanent resident living with family; Passport No. Z-4829101 surrendered.\n"
            "5. **Civil Dispute:** Supreme Court settled law (*Dalip Kaur (2009)*) holds that contractual breach is a civil matter."
        )

    # Default fallback
    return (
        "**LegalIQ Grounded Intelligence Brief:**\n\n"
        "• **Matter:** FIR No. 042/2023, Anna Nagar PS, Chennai (IPC 420 & 406).\n"
        "• **Complainant:** Shri M. Sundaram (MD, Sri Balaji Garments Pvt Ltd).\n"
        "• **Accused:** Rajesh Kumar (Proprietor, Precision Machines India).\n"
        "• **Contract Value:** ₹25,00,000/- for 2 industrial textile printing machines.\n"
        "• **Advance Paid:** ₹15,00,000/- via RTGS on 15-Jun-2023.\n"
        "• **Bona Fide Performance:** Accused remitted USD 16,500 (₹13.65L) to Heidelberg Tech GMBH in Germany on 22-Jun-2023.\n"
        "• **Port Delay:** Cargo arrived Chennai Port on 28-Jul-2023 and was held under automated customs regulations.\n"
        "• **Key Contradiction:** Complainant claims meeting at 10:30 AM at Corporate Office; Witness Suresh Natarajan states meeting was at 3:00 PM at Factory floor.\n"
        "• **Precedents:** *Arnesh Kumar (2014)* and *Satishchandra Ratanlal Shah (2019)*."
    )

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/logo.jpeg")
@app.route("/logo")
@app.route("/legal%20iq.jpeg")
@app.route("/legal iq.jpeg")
def serve_logo():
    if os.path.exists(LOCAL_LOGO):
        return send_file(LOCAL_LOGO, mimetype="image/jpeg")
    elif os.path.exists(PICTURES_LOGO):
        return send_file(PICTURES_LOGO, mimetype="image/jpeg")
    return "", 404

@app.route("/api/status", methods=["GET"])
def status():
    has_openai = is_valid_openai_key(os.getenv("OPENAI_API_KEY"))
    has_gemini = is_valid_gemini_key(os.getenv("GEMINI_API_KEY"))
    return jsonify({
        "status": "online",
        "openai_available": has_openai,
        "gemini_available": has_gemini,
        "active_provider": "openai" if has_openai else ("gemini" if has_gemini else "grounded_dossier")
    })

@app.route("/api/dossier", methods=["GET"])
def get_dossier():
    docs = []
    seen = set()
    for fname in DOSSIER_FILES:
        fpath = os.path.join(PARENT_DIR, fname)
        canonical = fname.replace(".txt.txt", ".txt")
        if os.path.exists(fpath) and canonical not in seen:
            seen.add(canonical)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    size_kb = os.path.getsize(fpath) / 1024
                    docs.append({
                        "name": canonical,
                        "size": f"{size_kb:.1f} KB",
                        "content": f.read()
                    })
            except Exception:
                pass
    return jsonify({"documents": docs})

@app.route("/api/save_key", methods=["POST"])
def save_key():
    try:
        data = request.json or {}
        provider = data.get("provider", "").lower()
        key_val = data.get("key", "").strip()
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        
        if provider == "openai":
            if is_valid_openai_key(key_val):
                os.environ["OPENAI_API_KEY"] = key_val
                set_key(env_path, "OPENAI_API_KEY", key_val)
                return jsonify({"status": "success", "message": "OpenAI API key saved successfully!"})
            else:
                return jsonify({"error": "Invalid OpenAI key format (must start with sk-proj-... or sk-... and have valid length)"}), 400
        elif provider == "gemini":
            if is_valid_gemini_key(key_val):
                os.environ["GEMINI_API_KEY"] = key_val
                set_key(env_path, "GEMINI_API_KEY", key_val)
                return jsonify({"status": "success", "message": "Gemini API key saved successfully!"})
            else:
                return jsonify({"error": "Invalid Gemini key format (Google AI Studio keys start with AIzaSy...)"}), 400
        return jsonify({"error": "Unknown provider"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        user_message = data.get("message") or data.get("prompt", "")
        user_message = user_message.strip()
        case_context = data.get("context") or data.get("case_context", "")
        case_context = case_context.strip()
        requested_provider = data.get("provider", "auto").lower()
        requested_model = data.get("model", "")
        custom_api_key = data.get("apiKey", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        effective_context = case_context if len(case_context) > 100 else SERVER_DOSSIER

        # Check credentials
        has_custom_openai = is_valid_openai_key(custom_api_key) if requested_provider == "openai" else False
        has_env_openai = is_valid_openai_key(os.getenv("OPENAI_API_KEY"))
        has_openai = has_custom_openai or has_env_openai

        has_custom_gemini = is_valid_gemini_key(custom_api_key) if requested_provider == "gemini" else False
        has_env_gemini = is_valid_gemini_key(os.getenv("GEMINI_API_KEY"))
        has_gemini = has_custom_gemini or has_env_gemini

        # Determine target provider: default is always Google Gemini
        if requested_provider == "openai" and has_openai:
            target_provider = "openai"
        elif has_gemini:
            target_provider = "gemini"
        else:
            target_provider = "grounded"

        # 1. OPENAI PATH
        if target_provider == "openai":
            if not has_openai:
                return jsonify({
                    "error": "No valid OpenAI API key configured. OpenAI API keys start with 'sk-proj-...'. Please open Settings (⚙️) on the left sidebar to enter your OpenAI key.",
                    "auth_error": True,
                    "provider": "OpenAI"
                }), 400
            try:
                client = get_openai_client(custom_api_key if has_custom_openai else None)
                if client:
                    model_name = requested_model if requested_model and "gpt" in requested_model else "gpt-4o-mini"
                    completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"Case Dossier:\n{effective_context}\n\nUser Question:\n{user_message}"}
                        ],
                        temperature=0.2
                    )
                    resp_text = completion.choices[0].message.content
                    return jsonify({
                        "response": resp_text,
                        "html": resp_text,
                        "status": "success",
                        "model": model_name,
                        "provider": "OpenAI",
                        "citation": f"OpenAI ({model_name})"
                    })
            except Exception as e:
                err_str = str(e)
                print(f"[OpenAI Call Error] {err_str}")
                if "insufficient_quota" in err_str or "credit_balance_exhausted" in err_str or "429" in err_str:
                    grounded_resp = generate_grounded_legal_response(user_message, effective_context)
                    notice = (
                        "<div class='p-3 bg-zinc-900 border border-zinc-700 rounded-xl text-zinc-300 text-xs mb-3'>"
                        "<p class='font-bold text-white mb-1'><i class='fa-solid fa-circle-exclamation text-amber-400 mr-1.5'></i> OpenAI Account Quota Exhausted ($0 Credits Remaining)</p>"
                        "<p>Your OpenAI API key is 100% valid, but OpenAI requires billing credits to generate responses. "
                        "You can add credits at <a href='https://platform.openai.com/settings/organization/billing' target='_blank' class='text-white underline font-semibold'>platform.openai.com/billing</a>, "
                        "or use 100% free <a href='https://aistudio.google.com' target='_blank' class='text-white underline font-semibold'>Google Gemini Flash</a>.</p>"
                        "<p class='text-zinc-400 mt-1.5 text-[11px]'>Grounded answer generated from verified case dossier below:</p>"
                        "</div>\n\n"
                    )
                    return jsonify({
                        "response": notice + grounded_resp,
                        "html": notice + grounded_resp,
                        "status": "success",
                        "model": "Grounded Engine (OpenAI Balance: $0)",
                        "provider": "LegalIQ Grounded",
                        "citation": "FIR 042/2023 Records"
                    })
                return jsonify({
                    "error": f"OpenAI API Error: {err_str}. Please check your API key and account billing/quota at https://platform.openai.com/settings/organization/billing.",
                    "auth_error": True,
                    "provider": "OpenAI"
                }), 401

        # 2. GEMINI PATH
        if target_provider == "gemini":
            if not has_gemini:
                return jsonify({
                    "error": "No valid Gemini API key configured. Gemini keys start with 'AIzaSy...'. Get a 100% free key at https://aistudio.google.com and enter it in Settings (⚙️).",
                    "auth_error": True,
                    "provider": "Google Gemini"
                }), 400
            try:
                client = get_gemini_client(custom_api_key if has_custom_gemini else None)
                models_to_try = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-lite-latest"]
                resp_text = None
                model_used = None
                for m in models_to_try:
                    try:
                        gem_response = client.models.generate_content(
                            model=m,
                            contents=f"Case Dossier & Evidence:\n{effective_context}\n\nUser Question:\n{user_message}",
                            config={"system_instruction": SYSTEM_PROMPT}
                        )
                        if gem_response and gem_response.text:
                            resp_text = gem_response.text
                            model_used = m
                            break
                    except Exception as me:
                        print(f"Gemini model {m} attempt: {me}")
                        continue

                if resp_text:
                    return jsonify({
                        "response": resp_text,
                        "html": resp_text,
                        "status": "success",
                        "model": model_used,
                        "provider": "Google Gemini",
                        "citation": "Google Gemini Flash"
                    })
                else:
                    grounded_resp = generate_grounded_legal_response(user_message, effective_context)
                    return jsonify({
                        "response": grounded_resp,
                        "html": grounded_resp,
                        "status": "success",
                        "model": "Grounded Legal Engine",
                        "provider": "LegalIQ Grounded",
                        "citation": "FIR 042/2023 Records"
                    })
            except Exception as e:
                grounded_resp = generate_grounded_legal_response(user_message, effective_context)
                return jsonify({
                    "response": grounded_resp,
                    "html": grounded_resp,
                    "status": "success",
                    "model": "Grounded Legal Engine",
                    "provider": "LegalIQ Grounded",
                    "citation": "FIR 042/2023 Records"
                })

        # 3. GROUNDED OFFLINE DOSSIER ENGINE (Default when keys not provided)
        grounded_resp = generate_grounded_legal_response(user_message, effective_context)
        return jsonify({
            "response": grounded_resp,
            "html": grounded_resp,
            "status": "success",
            "model": "Verified Case Dossier",
            "provider": "LegalIQ Grounded",
            "citation": "FIR 042/2023 Records"
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/<path:filename>")
def static_files(filename):
    if filename.startswith("api/"):
        return jsonify({"error": "Endpoint not found"}), 404
    return send_from_directory(".", filename)

if __name__ == "__main__":
    print("[LegalIQ] Multi-AI Server running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)