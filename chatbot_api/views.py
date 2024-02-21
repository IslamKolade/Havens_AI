from django.shortcuts import render
import os
from django.conf import settings
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt


file_path = os.path.join(settings.BASE_DIR, 'test_data.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    raw_text = file.read()

# Optimize text splitting
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

texts = text_splitter.split_text(raw_text)

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Build vector search index
docsearch = FAISS.from_texts(texts, embeddings)

# Load question answering chain
chain = load_qa_chain(OpenAI(), chain_type="stuff")

# Function to search for the response
def search_response(prompt):
    docs = docsearch.similarity_search(prompt)
    return chain.run(input_documents=docs, question=prompt)


def havens_ai(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = search_response(prompt)
        context= {
            'response': response,
            'prompt': prompt,
        }
        return JsonResponse(context)
        #return render(request, 'index.html', context)
    return render(request, 'index.html')
    #return HttpResponseForbidden()




