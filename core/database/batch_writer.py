import logging
from collections import deque

logger = logging.getLogger(__name__)

class BatchWriter:
    def __init__(self, db_manager, table_name, columns, max_buffer=500):
        self.db = db_manager
        self.table_name = table_name
        self.columns = columns
        self.max_buffer = max_buffer
        self.buffer = deque(maxlen=max_buffer)
        
        placeholders = ', '.join(['?'] * len(columns))
        col_names = ', '.join(columns)
        self.sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name, col_names, placeholders)
        
    def add(self, record: tuple):
        self.buffer.append(record)
        if len(self.buffer) >= self.max_buffer:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
            
        batch = []
        while self.buffer:
            batch.append(self.buffer.popleft())
            
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.executemany(self.sql, batch)
            conn.commit()
            
            logger.info('Flushed {} records to {}.'.format(len(batch), self.table_name))
            
        except Exception as e:
            logger.error('Failed to flush batch to {}: {}'.format(self.table_name, e))

    def shutdown(self):
        logger.info('Shutting down BatchWriter for {}, flushing remaining records...'.format(self.table_name))
        self.flush()