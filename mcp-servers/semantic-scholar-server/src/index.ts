#!/usr/bin/env node

/**
 * Semantic Scholar MCP Server
 * Provides access to Semantic Scholar research papers
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const SEMANTIC_SCHOLAR_API = 'https://api.semanticscholar.org/graph/v1';

class SemanticScholarServer {
  private server: Server;
  private apiKey: string | undefined;

  constructor() {
    this.apiKey = process.env.SEMANTIC_SCHOLAR_API_KEY;
    
    this.server = new Server(
      {
        name: 'semantic-scholar-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'search_papers',
          description: 'Search for research papers on Semantic Scholar',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query',
              },
              limit: {
                type: 'number',
                description: 'Maximum number of results (default: 10)',
                default: 10,
              },
              fields: {
                type: 'string',
                description: 'Comma-separated fields to return',
                default: 'title,authors,abstract,year,citationCount,url',
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'get_paper',
          description: 'Get details about a specific paper',
          inputSchema: {
            type: 'object',
            properties: {
              paperId: {
                type: 'string',
                description: 'Semantic Scholar paper ID or external ID (e.g., DOI, arXiv)',
              },
            },
            required: ['paperId'],
          },
        },
        {
          name: 'get_paper_citations',
          description: 'Get citations for a paper',
          inputSchema: {
            type: 'object',
            properties: {
              paperId: {
                type: 'string',
                description: 'Paper ID',
              },
              limit: {
                type: 'number',
                default: 10,
              },
            },
            required: ['paperId'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'search_papers') {
          return await this.searchPapers(args) as any;
        } else if (name === 'get_paper') {
          return await this.getPaper((args as any)?.paperId as string) as any;
        } else if (name === 'get_paper_citations') {
          return await this.getPaperCitations((args as any)?.paperId as string, (args as any)?.limit as number) as any;
        } else {
          throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [{ type: 'text', text: `Error: ${errorMessage}` }],
        } as any;
      }
    });
  }

  private async searchPapers(args: any) {
    const { query, limit = 10, fields = 'title,authors,abstract,year,citationCount,url' } = args;

    const url = new URL(`${SEMANTIC_SCHOLAR_API}/paper/search`);
    url.searchParams.append('query', query);
    url.searchParams.append('limit', limit.toString());
    url.searchParams.append('fields', fields);

    const headers: any = {};
    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey;
    }

    const response = await fetch(url.toString(), { headers });
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  private async getPaper(paperId: string) {
    const url = `${SEMANTIC_SCHOLAR_API}/paper/${paperId}?fields=title,authors,abstract,year,citationCount,referenceCount,url,venue,publicationDate`;

    const headers: any = {};
    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey;
    }

    const response = await fetch(url, { headers });
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  private async getPaperCitations(paperId: string, limit: number = 10) {
    const url = `${SEMANTIC_SCHOLAR_API}/paper/${paperId}/citations?limit=${limit}&fields=title,authors,year,citationCount`;

    const headers: any = {};
    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey;
    }

    const response = await fetch(url, { headers });
    const data = await response.json();

    return {
      content: [{ type: 'text', text: JSON.stringify(data, null, 2) }],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Semantic Scholar MCP Server running on stdio');
  }
}

const server = new SemanticScholarServer();
server.run().catch(console.error);

