import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import requests
import pandas as pd
import io
from api_keys import CLIENT_ID
from api_keys import CLIENT_SECRET

# Get the authorization token using the API key
def get_token():
    url = "https://apigtwb2c.us.dell.com/auth/oauth/v2/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')

# Get the warranty information about one item passed in with the token
def fetch_warranty(service_tag, token):
    url = f"https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements?servicetags={service_tag}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception:
        return {"error": "Invalid response", "raw": response.text}

# Extract the relevant information from the JSON response
def extract_summary(data):
    if isinstance(data, dict) and "error" in data:
        return [data]

    summary = []
    for item in data:
        entitlements = item.get('entitlements', [])
        latest_end = None
        if entitlements:
            latest_end = max(
                (datetime.fromisoformat(e['endDate'].replace('Z', '')) for e in entitlements if 'endDate' in e),
                default=None
            )
        summary.append({ # Create the output text for the GUI
            "Service Tag": item.get("serviceTag"),
            "Model": item.get("productLineDescription"),
            "Warranty End": latest_end.strftime('%Y-%m-%d') if latest_end else None
        })

    return summary

# This handles when there is more than one input in the GUI text box
def handle_batch():
    csv_text = input_text.get("1.0", tk.END).strip() 
    if not csv_text: # csv_text has the list of all inputs, as a string with \n after each one
        messagebox.showwarning("Input Error", "Please paste CSV content.")
        return
    try:
        df = pd.read_csv(io.StringIO(csv_text), header=None) 
        tags = df.iloc[:, 0].dropna().astype(str).tolist()
        tagList = [t[-7:] for t in tags if len(t) > 6] # Go through the input list and slice the last 7 characters, which is the service tag.

    except Exception as e:
        messagebox.showerror("CSV Error", f"Could not parse CSV: {e}")
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Processing batch lookup...\n") # Show that something is happening
    root.update_idletasks()  # Force GUI to update

    token = get_token()
    results = []
    for tag in tagList:
        raw = fetch_warranty(tag, token)
        summary = extract_summary(raw)
        results.extend(summary)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, pd.DataFrame(results).to_markdown(index=False)) # Display the text and make it a basic table format

# GUI Setup
root = tk.Tk()
root.title("Dell Warranty Lookup")
root.geometry("700x600")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Dell Warranty Lookup Tool", font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(pady=(10, 0))

mode_frame = tk.Frame(root, bg="#f0f0f0")
mode_frame.pack(pady=5)

btn_style = {
    "font": ("Segoe UI", 10),
    "bg": "#0078D7",
    "fg": "white",
    "activebackground": "#005A9E",
    "activeforeground": "white",
    "relief": tk.RAISED,
    "bd": 2,
    "width": 20,
    "padx": 5,
    "pady": 5
}

tk.Button(mode_frame, text="Submit", command=handle_batch, **btn_style).pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Input (1-100 computer names/service tags, comma or enter separated):", font=("Segoe UI", 10), bg="#f0f0f0").pack(pady=(10, 0))
input_text = scrolledtext.ScrolledText(root, height=6, width=80, relief=tk.SOLID, bd=2)
input_text.pack(padx=10, pady=5)

tk.Label(root, text="Output:", font=("Segoe UI", 10), bg="#f0f0f0").pack(pady=(10, 0))
output_text = scrolledtext.ScrolledText(root, height=15, width=80, relief=tk.SOLID, bd=2)
output_text.pack(padx=10, pady=5)

root.mainloop()
