from difflib import SequenceMatcher

def score_chunks_by_query(chunks, query, threshold=0.3):
    def score(chunk):
        return SequenceMatcher(None, chunk.lower(), query.lower()).ratio()

    scored = sorted(chunks, key=score, reverse=True)
    return [chunk for chunk in scored if score(chunk) >= threshold][:5]