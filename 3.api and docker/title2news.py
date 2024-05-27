from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Generate Article
def generate_article(title, model, tokenizer, max_length=512):
    input_text = f"Title: {title}\nArticle:"
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    article = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return article.replace(input_text, '').strip()

# # Load the model and tokenizer
# model = GPT2LMHeadModel.from_pretrained('retrained_model')
# tokenizer = GPT2Tokenizer.from_pretrained('retrained_model')
#
# # Example title to generate article
# new_title = "Nepal lost to west indies by 60 runs"
# generated_article = generate_article(new_title, model, tokenizer)
# print(generated_article)

def gen_article(title):
    # Load the model and tokenizer
    model = GPT2LMHeadModel.from_pretrained('retrained_model')
    tokenizer = GPT2Tokenizer.from_pretrained('retrained_model')

    # Example title to generate article
    # new_title = "Nepal lost to west indies by 60 runs"
    generated_article = generate_article(title, model, tokenizer)
    print(generated_article)
    return  generated_article