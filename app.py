import gradio as gr
from agent import rank_candidates
from data_loader import prepare_candidates
from email_agent import contact_candidate
from email_agent import generate_email_content, send_email
import json

current_job_description = ""
current_ranked = []

def make_overlay(percent, message, done=False):
    color = "#22c55e" if done else "#6366f1"
    spinner = "" if done else """
        <div style="width:52px;height:52px;border:5px solid #e5e7eb;border-top:5px solid #6366f1;
            border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 20px auto;"></div>
        <style>@keyframes spin{to{transform:rotate(360deg);}}</style>
    """

    auto_hide_style = """
        <style>
            #overlay-wrapper {
                animation: fadeOut 0.4s ease 0.5s forwards;
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to   { opacity: 0; pointer-events: none; }
            }
        </style>
    """ if done else ""

    html = f"""
    {auto_hide_style}
    <div id="overlay-wrapper" style="display:flex;position:fixed;top:0;left:0;width:100%;height:100%;
        background:rgba(0,0,0,0.65);z-index:9999;justify-content:center;align-items:center;">
        <div style="background:white;border-radius:20px;padding:44px 56px;text-align:center;
            box-shadow:0 24px 64px rgba(0,0,0,0.35);min-width:360px;">
            {spinner}
            <div style="font-size:21px;font-weight:700;color:#1e1b4b;margin-bottom:6px;">
                {"🎉 Analysis Complete!" if done else "🤖 AI Recruiter Working..."}
            </div>
            <div style="font-size:13px;color:#6b7280;margin-bottom:22px;">{message}</div>
            <div style="background:#e5e7eb;border-radius:999px;height:13px;overflow:hidden;margin-bottom:10px;">
                <div style="height:100%;width:{percent}%;
                    background:linear-gradient(90deg,{color},{'#16a34a' if done else '#8b5cf6'});
                    border-radius:999px;transition:width 0.4s ease;"></div>
            </div>
            <div style="font-size:13px;color:#4b5563;font-weight:600;">{percent}% complete</div>
        </div>
    </div>
    """
    return gr.update(value=html, visible=True)


def make_cards(ranked):
    """Build responsive candidate cards HTML."""
    n = len(ranked)


    if n <= 5:
        cols = n  
    elif n <= 10:
        cols = 2  
    elif n <= 15:
        cols = 2  
    else:
        cols = 2  

    cards_html = ""
    for i, c in enumerate(ranked):
        score = c['score']
        if score >= 70:
            badge_color = "#22c55e"
            badge_bg = "#f0fdf4"
            rank_label = "🟢 Strong Match"
        elif score >= 40:
            badge_color = "#f59e0b"
            badge_bg = "#fffbeb"
            rank_label = "🟡 Partial Match"
        else:
            badge_color = "#ef4444"
            badge_bg = "#fef2f2"
            rank_label = "🔴 Weak Match"

        strengths = "".join(f'<li style="margin-bottom:3px;">✅ {s}</li>' for s in c['strengths'])
        gaps = "".join(f'<li style="margin-bottom:3px;">❌ {g}</li>' for g in c['gaps'])

        radius = 28
        circumference = 2 * 3.14159 * radius
        dash = circumference * score / 100
        gap = circumference - dash

        card = f"""
        <div style="
            background:white;
            border-radius:16px;
            padding:22px 20px;
            box-shadow:0 4px 20px rgba(0,0,0,0.08);
            border:1.5px solid #f1f5f9;
            display:flex;
            flex-direction:column;
            gap:12px;
            transition:transform 0.2s,box-shadow 0.2s;
            min-width:0;
        " onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 32px rgba(0,0,0,0.13)'"
           onmouseout="this.style.transform='none';this.style.boxShadow='0 4px 20px rgba(0,0,0,0.08)'">

            <!-- Header: rank + name + score circle -->
            <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
                <div>
                    <div style="font-size:11px;font-weight:700;color:#94a3b8;letter-spacing:1px;margin-bottom:2px;">
                        RANK #{i+1}
                    </div>
                    <div style="font-size:17px;font-weight:700;color:#1e293b;line-height:1.2;">
                        {c['name']}
                    </div>
                    <div style="margin-top:5px;">
                        <span style="font-size:11px;font-weight:600;color:{badge_color};
                            background:{badge_bg};padding:3px 9px;border-radius:999px;">
                            {rank_label}
                        </span>
                    </div>
                </div>
                <!-- Score circle -->
                <div style="position:relative;flex-shrink:0;">
                    <svg width="72" height="72" viewBox="0 0 72 72">
                        <circle cx="36" cy="36" r="{radius}" fill="none" stroke="#f1f5f9" stroke-width="7"/>
                        <circle cx="36" cy="36" r="{radius}" fill="none" stroke="{badge_color}" stroke-width="7"
                            stroke-dasharray="{dash:.1f} {gap:.1f}"
                            stroke-linecap="round"
                            transform="rotate(-90 36 36)"/>
                    </svg>
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                        text-align:center;line-height:1.1;">
                        <div style="font-size:16px;font-weight:800;color:#1e293b;">{score}</div>
                        <div style="font-size:9px;color:#94a3b8;font-weight:600;">/100</div>
                    </div>
                </div>
            </div>

            <hr style="border:none;border-top:1px solid #f1f5f9;margin:0;">

            <!-- Strengths -->
            <div>
                <div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.8px;margin-bottom:6px;">
                    STRENGTHS
                </div>
                <ul style="margin:0;padding-left:16px;font-size:12.5px;color:#0f172a;line-height:1.6;">
                    {strengths}
                </ul>
            </div>

            <!-- Gaps -->
            <div>
                <div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.8px;margin-bottom:6px;">
                    GAPS
                </div>
                <ul style="margin:0;padding-left:16px;font-size:12.5px;color:#0f172a;line-height:1.6;">
                    {gaps}
                </ul>
            </div>

            <!-- Verdict -->
            <div style="background:#f8fafc;border-radius:10px;padding:10px 12px;
                font-size:12.5px;color:#475569;font-style:italic;border-left:3px solid {badge_color};">
                💬 {c['recommendation']}
            </div>

            <!-- Contact Button -->
            <button
                onclick="handleContact({c['id']}, this)"
                style="width:100%;margin-top:4px;padding:11px;
                background:linear-gradient(90deg,#6366f1,#8b5cf6);
                color:white;border:none;border-radius:10px;
                font-size:13px;font-weight:600;cursor:pointer;
                transition:opacity 0.2s;"
                onmouseover="this.style.opacity='0.85'"
                onmouseout="this.style.opacity='1'">
                📧 Contact {c['name'].split()[0]}
            </button>
            <div id="status-{c['id']}"
                style="font-size:12px;text-align:center;margin-top:4px;min-height:16px;">
            </div>
        </div>
        """
        cards_html += card
        
    if n <= 5:
        grid_cols = f"repeat({n}, 1fr)"
    else:
        grid_cols = "repeat(2, 1fr)"

    wrapper = f"""
    <div style="margin-top:32px;">
        <h2 style="text-align:center;font-size:22px;font-weight:800;color:#6366f1;margin-bottom:20px;">
            🏆 Ranked Candidates <span style="font-size:14px;font-weight:500;color:#94a3b8;">({n} results)</span>
        </h2>
        <div style="display:grid;grid-template-columns:{grid_cols};gap:18px;width:100%;">
            {cards_html}
        </div>
    </div>
    """
    return wrapper

def run_recruiter(job_description, num_candidates):
    global current_job_description, current_ranked

    if not job_description.strip():
        yield (gr.update(value="", visible=False), "⚠️ Please enter a job description.",
               gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True))
        return

    yield (make_overlay(10, "📥 Connecting to Hugging Face dataset..."),
           "", gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False))

    candidates = prepare_candidates(limit=int(num_candidates))

    yield (make_overlay(45, f"✅ Loaded {len(candidates)} candidates! Sending to Morpheus AI..."),
           "", gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False))

    yield (make_overlay(65, "🤖 AI is analyzing and ranking resumes..."),
           "", gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False))

    ranked = rank_candidates(job_description, candidates)
    candidate_lookup = {candidate["id"]: candidate for candidate in candidates}
    ranked = [{**candidate_lookup.get(item["id"], {}), **item} for item in ranked]
    current_job_description = job_description
    current_ranked = ranked

    yield (make_overlay(90, "📊 Finalizing ranked results..."),
           "", gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False))

    cards = make_cards(ranked)

    yield (
        make_overlay(100, "✅ Done! Results ready.", done=True),
        cards,
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )

def contact_candidate_fn(candidate_id):
    global current_ranked, current_job_description
    candidate = next((c for c in current_ranked if c["id"] == int(candidate_id)), None)
    if not candidate:
        return "❌ Candidate not found."
    return contact_candidate(candidate, current_job_description)


def preview_email_fn(candidate_id_str):
    """Return candidate info and AI-generated draft as JSON string for the modal preview."""
    if not candidate_id_str or not candidate_id_str.strip():
        return ""
    try:
        payload = json.loads(candidate_id_str)
        candidate_id = payload.get("candidate_id", candidate_id_str)
    except Exception:
        candidate_id = candidate_id_str

    candidate = next((c for c in current_ranked if c["id"] == int(candidate_id)), None)
    if not candidate:
        return json.dumps({"error": "Candidate not found."})
    try:
        draft = generate_email_content(candidate, current_job_description)
        payload = {
            "candidate": {
                "name": candidate.get("name"),
                "current_role": candidate.get("current_role"),
                "years_experience": candidate.get("years_experience"),
                "location": candidate.get("location"),
                "email": candidate.get("email"),
                "phone": candidate.get("phone", ""),
                "summary": candidate.get("summary", ""),
                "education": candidate.get("education", []),
                "experience": candidate.get("experience", []),
                "skills": candidate.get("skills", {}),
                "certifications": candidate.get("certifications", []),
                "languages": candidate.get("languages", []),
                "score": candidate.get("score"),
                "strengths": candidate.get("strengths", []),
                "gaps": candidate.get("gaps", []),
                "recommendation": candidate.get("recommendation", "")
            },
            "draft": draft
        }
        return json.dumps(payload)
    except Exception as e:
        return json.dumps({"error": str(e)})


def modal_send_fn(payload_str):
    """Send edited email from modal. Expects JSON string: {candidate_id, subject, body}.
    Returns a user-friendly status message (and also updates the hidden contact result textbox)."""
    try:
        data = json.loads(payload_str)
        candidate_id = int(data.get("candidate_id"))
        subject = data.get("subject", "")
        body = data.get("body", "")
    except Exception as e:
        return (f"❌ Error: invalid payload ({e})", f"❌ Error: invalid payload ({e})")

    candidate = next((c for c in current_ranked if c["id"] == int(candidate_id)), None)
    if not candidate:
        msg = f"❌ Candidate {candidate_id} not found."
        return (msg, msg)

    try:
        success = send_email(candidate.get("email"), subject, body)
        if success:
            msg = f"✅ Email successfully sent to {candidate.get('name')} at {candidate.get('email')}"
            return (msg, msg)
        else:
            msg = f"❌ Failed to send email to {candidate.get('name')}"
            return (msg, msg)
    except Exception as e:
        msg = f"❌ Error: {str(e)}"
        return (msg, msg)

custom_css = """
#input-section {
    max-width: 720px;
    margin: 0 auto;
}

#contact-input-box {
    display: none !important;
}


#contact-result-box {
    display: none !important;
}

#preview-input-box, #preview-result-box, #modal-send-input-box, #modal-send-result-box {
    display: none !important;
}

/* Ensure modal uses the same font stack as Gradio's app theme */
#candidate-modal-overlay,
#candidate-modal-overlay *,
#candidate-modal,
#candidate-modal * {
    font-family: var(--font, Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif) !important;
}

#results-section {
    width: 100%;
}
footer { display: none !important; }


#results-section ul li,
#results-section ul li *,
.candidate-list-item {
    color: #0f172a !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}
"""

custom_js = """
function getContactButtons() {
    return Array.from(document.querySelectorAll('#results-section button[onclick*="handleContact("]'));
}

function setContactButtonsEnabled(enabled, activeButton) {
    getContactButtons().forEach((button) => {
        if (activeButton && button === activeButton) {
            return;
        }
        button.disabled = !enabled;
        button.style.opacity = enabled ? '1' : '0.45';
        button.style.cursor = enabled ? 'pointer' : 'not-allowed';
    });

    if (activeButton) {
        activeButton.disabled = !enabled;
        activeButton.style.opacity = enabled ? '1' : '0.7';
        activeButton.style.cursor = enabled ? 'pointer' : 'not-allowed';
    }
}

function handleContact(candidateId, btn) {
    if (btn.disabled) {
        return;
    }

    // Use preview flow: request AI draft, then show modal for editing & sending.
    const previewBox = document.getElementById('preview-input-box');
    const hiddenInput = previewBox && previewBox.querySelector('textarea, input');
    const resultBox = document.getElementById('preview-result-box');
    const resultField = resultBox && resultBox.querySelector('textarea, input');
    const originalLabel = btn.dataset.originalLabel || btn.textContent;

    btn.dataset.originalLabel = originalLabel;

    if (!hiddenInput) {
        console.error('Preview input box not found.');
        return;
    }

    setContactButtonsEnabled(false, btn);

    // Clear any previous preview result to avoid stale data
    if (resultField) {
        try {
            const clearSetter = Object.getOwnPropertyDescriptor(
                resultField.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype,
                'value'
            ).set;
            clearSetter.call(resultField, '');
            resultField.dispatchEvent(new Event('input', { bubbles: true }));
            resultField.dispatchEvent(new Event('change', { bubbles: true }));
        } catch (e) {
            console.warn('Could not clear preview result', e);
        }
    }

    // Request AI draft for this candidate. Include a nonce so clicking the same
    // candidate again still triggers a fresh Gradio change event.
    const value = JSON.stringify({ candidate_id: String(candidateId), request_id: Date.now() + Math.random() });
    const valueSetter = Object.getOwnPropertyDescriptor(
        hiddenInput.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype,
        'value'
    ).set;
    valueSetter.call(hiddenInput, value);
    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
    hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));

    btn.disabled = true;
    btn.style.opacity = '0.7';
    btn.textContent = '🔎 Preparing preview...';

    let seen = false;
    const watcher = setInterval(() => {
        if (!resultField) return;
        const payload = resultField.value || '';
        if (!payload || seen) return;
        seen = true;
        clearInterval(watcher);

        let data = null;
        try {
            data = JSON.parse(payload);
        } catch (e) {
            console.error('Invalid preview payload', e);
            btn.textContent = originalLabel;
            setContactButtonsEnabled(true, btn);
            return;
        }

        if (data.error) {
            btn.textContent = '❌ Preview failed';
            setContactButtonsEnabled(true, btn);
            return;
        }

        // Build modal DOM
        if (document.getElementById('candidate-modal-overlay')) {
            document.getElementById('candidate-modal-overlay').remove();
        }

        const overlay = document.createElement('div');
        overlay.id = 'candidate-modal-overlay';
        overlay.style = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:99999;';

        const modal = document.createElement('div');
        modal.id = 'candidate-modal';
        modal.style = 'background:white;border-radius:12px;padding:18px 20px;max-width:760px;width:92%;max-height:80vh;overflow:auto;position:relative;';

        const closeBtn = document.createElement('button');
        closeBtn.innerText = '✖';
        closeBtn.style = 'position:absolute;right:12px;top:10px;border:none;background:transparent;font-size:18px;cursor:pointer;';
        closeBtn.onclick = () => { overlay.remove(); btn.textContent = originalLabel; setContactButtonsEnabled(true, btn); if (resultField) { try { const cs = Object.getOwnPropertyDescriptor(resultField.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype, 'value').set; cs.call(resultField, ''); resultField.dispatchEvent(new Event('input', { bubbles: true })); resultField.dispatchEvent(new Event('change', { bubbles: true })); } catch(e){}} };
        modal.appendChild(closeBtn);

        const title = document.createElement('div');
        title.innerHTML = `<h3 style="margin:6px 0 8px 0;color:#111827;font-size:18px;">Contact Preview — ${data.candidate.name}</h3>`;
        modal.appendChild(title);

        // Candidate info
        const info = document.createElement('div');
        info.style = 'font-size:13px;color:#374151;margin-bottom:12px;';
        const ci = data.candidate;

        const makeSection = (label, items) => {
            if (!items || !items.length) return null;
            const section = document.createElement('div');
            section.style = 'margin-bottom:10px;';
            const heading = document.createElement('div');
            heading.innerText = label;
            heading.style = 'font-weight:700;margin-bottom:4px;color:#111827;';
            const list = document.createElement('ul');
            list.style = 'margin:0 0 0 16px;padding:0;';
            items.forEach(text => {
                const li = document.createElement('li');
                li.style = 'margin-bottom:4px;';
                li.innerText = text;
                list.appendChild(li);
            });
            section.appendChild(heading);
            section.appendChild(list);
            return section;
        };

        const overviewItems = [
            `Name: ${ci.name}`,
            `Current role: ${ci.current_role || '-'}`,
            `Years experience: ${ci.years_experience || '-'}`,
            `Location: ${ci.location || '-'}`,
            `Email: ${ci.email || '-'}`,
            `Phone: ${ci.phone || '-'}`,
            `Match score: ${ci.score || '-'}`,
        ];
        const overview = makeSection('Candidate Overview', overviewItems);
        if (overview) info.appendChild(overview);

        const skillGroups = ci.skills || {};
        const groupedSkills = [];
        if (skillGroups.technical && skillGroups.technical.length) groupedSkills.push(`Technical: ${skillGroups.technical.join(', ')}`);
        if (skillGroups.tools && skillGroups.tools.length) groupedSkills.push(`Tools: ${skillGroups.tools.join(', ')}`);
        if (skillGroups.soft_skills && skillGroups.soft_skills.length) groupedSkills.push(`Soft skills: ${skillGroups.soft_skills.join(', ')}`);
        const skillsSection = makeSection('Skills & Tools', groupedSkills);
        if (skillsSection) info.appendChild(skillsSection);

        const certSection = makeSection('Certifications', (ci.certifications || []).map(item => item));
        if (certSection) info.appendChild(certSection);

        const langSection = makeSection('Languages', (ci.languages || []).map(item => item));
        if (langSection) info.appendChild(langSection);

        const strengthsSection = makeSection('Strengths', (ci.strengths || []).map(item => `✅ ${item}`));
        if (strengthsSection) info.appendChild(strengthsSection);

        const gapsSection = makeSection('Gaps', (ci.gaps || []).map(item => `❌ ${item}`));
        if (gapsSection) info.appendChild(gapsSection);

        if (ci.summary) {
            const summarySection = document.createElement('div');
            summarySection.style = 'margin-bottom:10px;';
            summarySection.innerHTML = `<div style="font-weight:700;margin-bottom:4px;color:#111827;">Summary</div><div style="line-height:1.55;color:#374151;">${ci.summary}</div>`;
            info.appendChild(summarySection);
        }

        modal.appendChild(info);

        // Subject
        const subjLabel = document.createElement('div');
        subjLabel.innerText = 'Subject';
        subjLabel.style = 'font-weight:700;margin-bottom:6px;color:#111827;';
        modal.appendChild(subjLabel);
        const subjArea = document.createElement('textarea');
        subjArea.id = 'candidate-modal-subject';
        subjArea.style = 'width:100%;min-height:40px;padding:10px;border-radius:8px;border:1px solid #e6e9ee;margin-bottom:12px;';
        subjArea.value = data.draft.subject || '';
        modal.appendChild(subjArea);

        // Body
        const bodyLabel = document.createElement('div');
        bodyLabel.innerText = 'Email';
        bodyLabel.style = 'font-weight:700;margin-bottom:6px;color:#111827;';
        modal.appendChild(bodyLabel);
        const bodyArea = document.createElement('textarea');
        bodyArea.id = 'candidate-modal-body';
        bodyArea.style = 'width:100%;min-height:160px;padding:12px;border-radius:8px;border:1px solid #e6e9ee;margin-bottom:12px;font-size:14px;line-height:1.45;';
        bodyArea.value = data.draft.body || '';
        modal.appendChild(bodyArea);

        // Buttons
        const footer = document.createElement('div');
        footer.style = 'display:flex;gap:8px;justify-content:flex-end;';
        const cancelBtn = document.createElement('button');
        cancelBtn.innerText = 'Cancel';
        cancelBtn.style = 'padding:10px 14px;border-radius:8px;border:1px solid #e5e7eb;background:white;cursor:pointer;';
        cancelBtn.onclick = () => { overlay.remove(); btn.textContent = originalLabel; setContactButtonsEnabled(true, btn); if (resultField) { try { const cs = Object.getOwnPropertyDescriptor(resultField.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype, 'value').set; cs.call(resultField, ''); resultField.dispatchEvent(new Event('input', { bubbles: true })); resultField.dispatchEvent(new Event('change', { bubbles: true })); } catch(e){} } };
        footer.appendChild(cancelBtn);

        const sendBtn = document.createElement('button');
        sendBtn.id = 'candidate-modal-send';
        sendBtn.innerText = 'Send Email';
        sendBtn.style = 'padding:10px 14px;border-radius:8px;border:none;background:linear-gradient(90deg,#6366f1,#8b5cf6);color:white;cursor:pointer;font-weight:700;';
        footer.appendChild(sendBtn);
        modal.appendChild(footer);

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Send handler
        sendBtn.onclick = () => {
            sendBtn.disabled = true;
            sendBtn.innerText = '⏳ Sending...';
            const sendBox = document.getElementById('modal-send-input-box');
            const sendHidden = sendBox && sendBox.querySelector('textarea, input');
            if (!sendHidden) {
                console.error('Modal send box missing');
                return;
            }
            const payload = JSON.stringify({ candidate_id: candidateId, subject: subjArea.value, body: bodyArea.value });
            const vs = Object.getOwnPropertyDescriptor(
                sendHidden.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype,
                'value'
            ).set;
            vs.call(sendHidden, payload);
            sendHidden.dispatchEvent(new Event('input', { bubbles: true }));
            sendHidden.dispatchEvent(new Event('change', { bubbles: true }));

            // watch for send result
            const sendWatcher = setInterval(() => {
                const sendResBox = document.getElementById('modal-send-result-box');
                const sendResField = sendResBox && sendResBox.querySelector('textarea, input');
                if (!sendResField) return;
                const r = sendResField.value || '';
                if (!r) return;
                clearInterval(sendWatcher);
                // propagate to contact-result-box so original button watcher updates
                const contactResBox = document.getElementById('contact-result-box');
                const contactResField = contactResBox && contactResBox.querySelector('textarea, input');
                if (contactResField) {
                    const s = Object.getOwnPropertyDescriptor(
                        contactResField.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype,
                        'value'
                    ).set;
                    s.call(contactResField, r);
                    contactResField.dispatchEvent(new Event('input', { bubbles: true }));
                    contactResField.dispatchEvent(new Event('change', { bubbles: true }));
                }
                // show brief confirmation then close
                sendBtn.innerText = '✅ Sent';
                setTimeout(() => { overlay.remove(); btn.textContent = '✅ Sent successfully'; setContactButtonsEnabled(true); if (resultField) { try { const cs = Object.getOwnPropertyDescriptor(resultField.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype, 'value').set; cs.call(resultField, ''); resultField.dispatchEvent(new Event('input', { bubbles: true })); resultField.dispatchEvent(new Event('change', { bubbles: true })); } catch(e){} } }, 700);
            }, 250);
        };
    }, 200);
}
"""

with gr.Blocks(title="🤖 Intelligent Recruiter") as demo:

    gr.Markdown("""
    <div style="text-align:center;padding:24px 0 8px 0;">
        <div style="font-size:36px;margin-bottom:8px;">🤖</div>
        <h1 style="font-size:28px;font-weight:800;color:#6366f1;margin:0;">Intelligent Recruiter Agent</h1>
        <p style="color:#64748b;margin-top:6px;font-size:15px;">Powered by Morpheus AI</p>
    </div>
    """)

    overlay = gr.HTML(value="", visible=False)

    with gr.Column(elem_id="input-section"):
        job_input = gr.Textbox(
            label="📋 Job Description",
            placeholder="Enter job title, requirements, skills needed...",
            lines=8
        )
        num_slider = gr.Slider(
            minimum=5, maximum=20, value=10, step=5,
            label="👥 Number of Candidates to Analyze"
        )
        run_btn = gr.Button("🚀 Find Best Candidates", variant="primary", size="lg")

        gr.Examples(
            examples=[
                ["Job Title: Senior Backend Engineer\n\nRequirements:\n- 5+ years Python\n- FastAPI or Django\n- PostgreSQL and Redis\n- Docker and Kubernetes", 10],
                ["Job Title: Data Scientist\n\nRequirements:\n- Machine learning experience\n- Python, TensorFlow or PyTorch\n- SQL and data visualization\n- Statistics background", 10],
                ["Job Title: Senior Java Developer\n\nRequirements:\n- 4+ years Java experience\n- Spring Boot and Microservices\n- REST API development\n- MySQL or PostgreSQL", 10],
            ],
            inputs=[job_input, num_slider],
            label="💡 Example Job Descriptions (click to try)"
        )

    with gr.Column(elem_id="results-section"):
        output = gr.HTML(label="Results")
        contact_result = gr.Textbox(
            value="",
            visible=True,
            show_label=False,
            container=True,
            interactive=False,
            elem_id="contact-result-box"
        )

        # Hidden preview/send bridges for modal flow
        preview_input = gr.Textbox(
            value="",
            visible=True,
            show_label=False,
            container=True,
            elem_id="preview-input-box"
        )
        preview_result = gr.Textbox(
            value="",
            visible=True,
            show_label=False,
            container=True,
            interactive=False,
            elem_id="preview-result-box"
        )

        modal_send_input = gr.Textbox(
            value="",
            visible=True,
            show_label=False,
            container=True,
            elem_id="modal-send-input-box"
        )
        modal_send_result = gr.Textbox(
            value="",
            visible=True,
            show_label=False,
            container=True,
            interactive=False,
            elem_id="modal-send-result-box"
        )

    contact_input = gr.Textbox(
        value="",
        visible=True,
        show_label=False,
        container=True,
        elem_id="contact-input-box"
    )

    def handle_contact_click(candidate_id_str):
        if not candidate_id_str.strip():
            return gr.update(value="")
        try:
            result = contact_candidate_fn(candidate_id_str.strip())
            return gr.update(value=result)
        except Exception as e:
            return gr.update(value=f"❌ Error: {str(e)}")

    contact_input.change(
        fn=handle_contact_click,
        inputs=[contact_input],
        outputs=[contact_result]
    )

    preview_input.change(
        fn=preview_email_fn,
        inputs=[preview_input],
        outputs=[preview_result]
    )

    modal_send_input.change(
        fn=modal_send_fn,
        inputs=[modal_send_input],
        outputs=[modal_send_result, contact_result]
    )

    run_btn.click(
        fn=run_recruiter,
        inputs=[job_input, num_slider],
        outputs=[overlay, output, job_input, num_slider, run_btn]
    )

demo.launch(theme=gr.themes.Soft(), css=custom_css, js=custom_js)