from flask import Flask, render_template, request, redirect, url_for
import openai

client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__)
posts = []

def generate_article(title):
    prompt = f"اكتب مقالا مفصلا واحترافيا حول '{title}' باللغة العربية."

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "أنت كاتب مقالات محترف باللغة العربية."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = generate_article(title)
        new_id = len(posts) + 1
        posts.append({"id": new_id, "title": title, "content": content})
        return redirect(url_for('home'))
    return render_template('add_post.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    article = next((p for p in posts if p["id"] == post_id), None)
    if article:
        return render_template('post.html', post=article)
    else:
        return "المقال غير موجود", 404

if __name__ == "__main__":
    app.run(debug=True)
