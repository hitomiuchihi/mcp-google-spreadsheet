
import { Mastra } from '@mastra/core/mastra';
import { createLogger } from '@mastra/core/logger';
import { LibSQLStore } from '@mastra/libsql';
import { weatherWorkflow } from './workflows';
import { multiAgent } from './agents';

export const mastra = new Mastra({
  // 使用可能なワークフロー
  workflows: { weatherWorkflow },

  // 使用可能なエージェント
  agents: { multiAgent },

  // ストレージ: LibSQLStoreを使用して、SQLiteデータベースに保存
  storage: new LibSQLStore({
    // stores telemetry, evals, ... into memory storage, if it needs to persist, change to file:../mastra.db
    url: ":memory:",
  }),

  // ログ
  logger: createLogger({
    name: 'Mastra',
    level: 'info',
  }),
});
