from models import *
from forms import *
from logic import *

# Render the main screen
@app.route('/', methods=['GET','POST'])
def postsPost():

    post_form = PostForm()
    request_ip = request.environ['HTTP_X_FORWARDED_FOR']
    
    ip_hash = createIdHash(request_ip)
    sys_time = "%s" % strftime('%I:%M:%S %p')

    if post_form.validate_on_submit():
        
        text_content = post_form.text_content.data
        new_post = Post(content=str(text_content), ipHash=ip_hash, timestamp=sys_time)

        DB.session.add(new_post)
        DB.session.commit()
    
    all_posts = Post.query.all() # Get all posts
    
    # Delete the oldest post if post limit reached
    if len(all_posts) >= POST_LIMIT:
        DB.session.delete(all_posts[0])
        DB.session.commit()

    posted_data = {"posted": request.method == 'POST', "allposts": reversed(all_posts)}
    
    return render_template("index.html", post=posted_data, form=post_form, myIp=ip_hash)


@app.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    return redirect(url_for("postsPost"))


@app.route('/delete/<int:postId>')
def deleteId(postId):

    request_ip = request.environ['HTTP_X_FORWARDED_FOR']
    ip_hash = createIdHash(request_ip)

    toDeletePost = Post.query.get(postId)
    
    if toDeletePost and ip_hash == toDeletePost.ipHash:
        DB.session.delete(toDeletePost)
        DB.session.commit()
    
    return redirect(url_for("postsPost"))