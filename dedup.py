from itertools import chain
import sys

import pandas as pd
import numpy as np

chunker = pd.read_csv(sys.stdin, dtype={'lat': np.object_, 'long': np.object_}, chunksize=50000)

chunk_iter = iter(chunker)
peek = chunk_iter.next()
chunks = chain([peek], chunk_iter)

last = pd.DataFrame(columns=peek.columns)
dedup_cols = peek.columns.drop('lastUpdate')
ix_cols = ['lastUpdate', 'id']

for chunk in chunks:
    dedup = pd.concat([last, chunk]).drop_duplicates(cols=dedup_cols).drop_duplicates()
    dedup_ix = dedup.set_index(ix_cols)
    chunk_ix = chunk.set_index(ix_cols)
    last_ix = last.set_index(ix_cols)
    dedup_ix.ix[dedup_ix.index.diff(last_ix.index)].to_csv(sys.stdout, header=False, float_format='%.0F')
    last = chunk
