import gradio as gr
from agent import rank_candidates
from data_loader import prepare_candidates

def run_recruiter(job_description, num_candidates):
    if not job_description.strip():
        yield (
            gr.update(visible=True,  value="⚠️ Please enter a job description."),
            gr.update(visible=False),
            gr.update(interactive=True),
            gr.update(interactive=True),
            gr.update(interactive=True),
        )
        return

    # Step 1
    yield (
        gr.update(visible=True, value="📥 Loading candidates from Hugging Face... (10%)"),
        gr.update(visible=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )

    candidates = prepare_candidates(limit=int(num_candidates))

    # Step 2
    yield (
        gr.update(visible=True, value=f"✅ Loaded {len(candidates)} candidates! Sending to Morpheus AI... (50%)"),
        gr.update(visible=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )

    ranked = rank_candidates(job_description, candidates)

    # Step 3
    yield (
        gr.update(visible=True, value="📊 Ranking candidates by best match... (85%)"),
        gr.update(visible=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )

    # Format output
    output = "# 🏆 Ranked Candidates\n\n"
    for i, c in enumerate(ranked):
        score = c['score']
        if score >= 70:
            emoji = "🟢"
        elif score >= 40:
            emoji = "🟡"
        else:
            emoji = "🔴"

        output += f"## {emoji} #{i+1} {c['name']} — Score: {score}/100\n"
        output += f"**✅ Strengths:** {', '.join(c['strengths'])}\n\n"
        output += f"**❌ Gaps:** {', '.join(c['gaps'])}\n\n"
        output += f"**💬 Verdict:** {c['recommendation']}\n\n"
        output += "---\n\n"

    # Done — hide status, show results, re-enable inputs
    yield (
        gr.update(visible=False, value=""),
        gr.update(visible=True, value=output),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


with gr.Blocks(title="🤖 Intelligent Recruiter", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🤖 Intelligent Recruiter Agent
    ### Powered by Morpheus AI × Hugging Face
    Enter a job description and let the AI find the best matching candidates!
    """)

    with gr.Row():
        with gr.Column():
            job_input = gr.Textbox(
                label="📋 Job Description",
                placeholder="Enter job title, requirements, skills needed...",
                lines=10
            )
            num_slider = gr.Slider(
                minimum=5,
                maximum=20,
                value=10,
                step=5,
                label="👥 Number of Candidates to Analyze"
            )
            run_btn = gr.Button(
                "🚀 Find Best Candidates",
                variant="primary"
            )

        with gr.Column():
            # Status box — shows progress messages while loading
            status_box = gr.Textbox(
                label="⏳ Status",
                interactive=False,
                visible=False,
                lines=2
            )
            # Output — hidden until results are ready
            output = gr.Markdown(
                visible=False
            )

    gr.Examples(
        examples=[
            ["Job Title: Senior Backend Engineer\n\nRequirements:\n- 5+ years Python\n- FastAPI or Django\n- PostgreSQL and Redis\n- Docker and Kubernetes", 10],
            ["Job Title: Data Scientist\n\nRequirements:\n- Machine learning experience\n- Python, TensorFlow or PyTorch\n- SQL and data visualization\n- Statistics background", 10],
            ["Job Title: Senior Java Developer\n\nRequirements:\n- 4+ years Java experience\n- Spring Boot and Microservices\n- REST API development\n- MySQL or PostgreSQL", 10],
        ],
        inputs=[job_input, num_slider],
        label="💡 Example Job Descriptions (click to try)"
    )

    run_btn.click(
        fn=run_recruiter,
        inputs=[job_input, num_slider],
        outputs=[status_box, output, job_input, num_slider, run_btn]
    )

demo.launch()