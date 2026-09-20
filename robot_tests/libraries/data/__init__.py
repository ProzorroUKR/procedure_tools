"""
Data builders for the Robot Framework tests.

Each module covers one part of a procedure and composes the ones below it:

- ``utils``    merging, overrides and the faker the CLI uses
- ``common``   addresses, organizations, items, lots, values, milestones
- ``document`` documents and the file content uploaded for them
- ``plan``     plans
- ``tender``   tenders and their config
- ``criteria`` tender criteria and the bid answers derived from them
- ``bid``      bids
- ``award``    awards
- ``contract`` contracts and their amendments

``ProcedureData`` exposes all of them as keywords; nothing here reads a file,
every payload is built in memory and handed straight to an action.
"""
