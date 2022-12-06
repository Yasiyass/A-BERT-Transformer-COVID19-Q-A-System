
from haystack.document_stores import ElasticsearchDocumentStore
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")


# Let's first fetch some documents that we want to query
import pandas as pd
df = pd.read_csv('FINAL_CORD_DATA.csv')
df.dropna(inplace=True)

# Convert files to dicts
# It must take a str as input, and return a str.
dicts = df.to_dict('records')

# Now, let's write the dicts containing documents to our DB.
final_dicts = []
for each in dicts:
    tmp = {}
    if each is not None:
        tmp['content'] = each.pop('body_text')
        tmp['meta'] = each
    final_dicts.append(tmp)

document_store.write_documents(final_dicts)
