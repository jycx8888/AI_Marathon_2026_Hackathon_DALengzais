import gradio as gr
from agent import rank_candidates
from data_loader import prepare_candidates

def make_overlay(percent, message, done=False):
    color = "#22c55e" if done else "#6366f1"
    spinner = "" if done else """
        <div style="width:52px;height:52px;border:5px solid #e5e7eb;border-top:5px solid #6366f1;
            border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 20px auto;"></div>
        <style>@keyframes spin{to{transform:rotate(360deg);}}</style>
    """

    # Auto-hide after 0.5s when done
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

    # Determine columns per row
    if n <= 5:
        cols = n  # all in one row
    elif n <= 10:
        cols = 2  # two per row → fills nicely
    elif n <= 15:
        cols = 2  # two rows: 8+7
    else:
        cols = 2  # two rows: 10+10

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

        # Arc progress circle (SVG)
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
                <ul style="margin:0;padding-left:16px;font-size:12.5px;color:#374151;line-height:1.6;">
                    {strengths}
                </ul>
            </div>

            <!-- Gaps -->
            <div>
                <div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.8px;margin-bottom:6px;">
                    GAPS
                </div>
                <ul style="margin:0;padding-left:16px;font-size:12.5px;color:#374151;line-height:1.6;">
                    {gaps}
                </ul>
            </div>

            <!-- Verdict -->
            <div style="background:#f8fafc;border-radius:10px;padding:10px 12px;
                font-size:12.5px;color:#475569;font-style:italic;border-left:3px solid {badge_color};">
                💬 {c['recommendation']}
            </div>
        </div>
        """
        cards_html += card

    # Determine grid columns CSS
    if n <= 5:
        grid_cols = f"repeat({n}, 1fr)"
    else:
        grid_cols = "repeat(2, 1fr)"

    wrapper = f"""
    <div style="margin-top:32px;">
        <h2 style="text-align:center;font-size:22px;font-weight:800;color:#1e293b;margin-bottom:20px;">
            🏆 Ranked Candidates <span style="font-size:14px;font-weight:500;color:#94a3b8;">({n} results)</span>
        </h2>
        <div style="display:grid;grid-template-columns:{grid_cols};gap:18px;width:100%;">
            {cards_html}
        </div>
    </div>
    """
    return wrapper


def run_recruiter(job_description, num_candidates):
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


custom_css = """
/* Center the top input section */
#input-section {
    max-width: 720px;
    margin: 0 auto;
}
/* Results fill full width */
#results-section {
    width: 100%;
}
footer { display: none !important; }
"""

with gr.Blocks(title="🤖 Intelligent Recruiter", theme=gr.themes.Soft(), css=custom_css) as demo:

    gr.Markdown("""
    <div style="text-align:center;padding:24px 0 8px 0;">
        <div style="font-size:36px;margin-bottom:8px;">🤖</div>
        <h1 style="font-size:28px;font-weight:800;color:#1e293b;margin:0;">Intelligent Recruiter Agent</h1>
        <p style="color:#64748b;margin-top:6px;font-size:15px;">Powered by Morpheus AI × Hugging Face</p>
    </div>
    """)

    overlay = gr.HTML(value="", visible=False)

    # ── Centered input section ───────────────────────────────────
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

    # ── Full-width results section ───────────────────────────────
    with gr.Column(elem_id="results-section"):
        output = gr.HTML(label="Results")

    run_btn.click(
        fn=run_recruiter,
        inputs=[job_input, num_slider],
        outputs=[overlay, output, job_input, num_slider, run_btn]
    )

demo.launch()