import streamlit as st
import streamlit.components.v1 as components

# Function to display blog post
def display_blog_post(title, content, font_size, font_family, text_color, background_color):
    st.markdown(f"""
        <div style="
            font-size: {font_size};
            font-family: {font_family};
            color: {text_color};
            background-color: {background_color};
            padding: 20px;
            border-radius: 10px;">
            <h2>{title}</h2>
            <div>{content}</div>
        </div>
    """, unsafe_allow_html=True)

# Main function
def main():
    st.title("Minimalist Blog Editor")

    # Sidebar for customization
    with st.sidebar:
        st.header("Customization")
        font_size = st.slider("Font Size", 12, 30, 16)
        font_family = st.selectbox("Font Family", ["Arial", "Helvetica", "Times New Roman", "Georgia"])
        text_color = st.color_picker("Text Color", "#000000")
        background_color = st.color_picker("Background Color", "#FFFFFF")

    # Input fields for blog post
    title = st.text_input("Blog Title", "My Awesome Blog Post")
    content = st.text_area("Blog Content", "Write your blog content here...", height=300)

    # Display the blog post
    display_blog_post(title, content, f"{font_size}px", font_family, text_color, background_color)

    # Store blog posts (for demonstration purposes)
    if 'blog_posts' not in st.session_state:
        st.session_state['blog_posts'] = []

    # Button to post the blog
    if st.button("Post Blog"):
        st.session_state['blog_posts'].append({
            'title': title,
            'content': content,
            'font_size': f"{font_size}px",
            'font_family': font_family,
            'text_color': text_color,
            'background_color': background_color
        })
        st.success("Blog posted successfully!")

    # Display published blogs
    st.header("Published Blogs")
    if st.session_state['blog_posts']:
        for post in st.session_state['blog_posts']:
            display_blog_post(post['title'], post['content'], post['font_size'], post['font_family'], post['text_color'], post['background_color'])
    else:
        st.info("No blogs posted yet.")

if __name__ == "__main__":
    main()
