from sqlalchemy.dialects.postgresql import insert


def upsert_dataframe(df, table, engine, pk):
    with engine.connect() as conn:
        for _, row in df.iterrows():
            stmt = insert(table).values(**row.to_dict())
            stmt = stmt.on_conflict_do_nothing(index_elements=[pk])
            conn.execute(stmt)
