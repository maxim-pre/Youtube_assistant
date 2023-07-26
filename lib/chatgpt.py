import os
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import YoutubeLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

# this loads the OPENAI_API_KEY from our .env file. The library that requires the apikey will recognise the name and use its value
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
print(OPENAI_API_KEY)

# this embeddings model is used to create a vector representation of a piece of text for OpenAI.
embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def create_db_from_youtube_video_url(url):
    # use langchain's document loaders to get a full transcript of a youtube video from it's url 
    loader = YoutubeLoader.from_youtube_url(url)
    transcript = loader.load() # contains the entire content of the video as a string "transcript[0].page_content"

    # video transcripts can contain hundres of thousands of characters so we need a way to break it up so we only use the parts with relevant info.
    # Here we are splitting the transcript into chunks of 1000 characters
    # RecursiveCharacterTextSplitter is recommended by Langchain for Generic text
    # It tries to keep paragraphs, sentences and words together as long as possible, as these would have the most semantically related info. 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    # creates an array of langchain document objects each with content containing characters equal to chunk size
    docs = text_splitter.split_documents(transcript)


    # Here I am Created a database of the vector representation of the documents using the embeddings model defined earlier
    # I am also using FAISS (Facebook AI Similariy Search) library so that when someone asks a question about the transcript
    # We can perform a silmilarity search to find the most relevant chunks
    db = FAISS.from_documents(docs, embeddings_model)
    
    return db

def get_response_from_query(db, query, k=4):
    # k is the number of documents we are allowing the ai to use to answer the query 
    # I will be using gpt-3.5-turbo which has a maximum tokens of 4096
    # setting k=4 therefore means we can utilise the token capacity (4 * 1000 = 4000)
    docs = db.similarity_search(query, k=k)

    # the following line is a string of the most relevant information in the transcript based on the given query
    docs_page_content = ' '.join([d.page_content for d in docs])

    # llm = OpenAI(model_name="gpt-3.5-turbo")
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)



    # here I am creating a prompt that I will send to the llm. 
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful assistant that can answers questions about youtube videos based on the videos transcript.
        
        Answer the following questions: {question}

        By Searching the following transcript: {docs}

        Only use Factual information from the transcript to answer the question.

        If you don't have enough information to answer the question, say "I don't know".

        Your answers should be verbose and detailed.

        """

    )

    # Here we are Creating a chain using Langchain's Chain class to combine the prompt we defined earlier with the llm.
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, docs=docs_page_content)
    return response


video_url = "https://www.youtube.com/watch?v=Ha0m9rPcbRU"
query = "what is this video about?"
db = create_db_from_youtube_video_url(video_url)
response = get_response_from_query(db, query)

print(response)
