#!/usr/bin/env node

/**
 * arXiv MCP Server
 * Provides access to arXiv research papers via MCP
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';
import { parseString } from 'xml2js';

interface ArxivSearchParams {
  query: string;
  maxResults?: number;
  sortBy?: 'relevance' | 'lastUpdatedDate' | 'submittedDate';
  sortOrder?: 'ascending' | 'descending';
}

class ArxivServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'arxiv-server',
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
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'search_arxiv',
          description: 'Search for research papers on arXiv',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Search query for arXiv papers',
              },
              maxResults: {
                type: 'number',
                description: 'Maximum number of results to return (default: 10)',
                default: 10,
              },
              sortBy: {
                type: 'string',
                enum: ['relevance', 'lastUpdatedDate', 'submittedDate'],
                description: 'Sort order for results',
                default: 'relevance',
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'get_arxiv_paper',
          description: 'Get detailed information about a specific arXiv paper',
          inputSchema: {
            type: 'object',
            properties: {
              paperId: {
                type: 'string',
                description: 'arXiv paper ID (e.g., 2301.12345)',
              },
            },
            required: ['paperId'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'search_arxiv') {
          const result = await this.searchArxiv(args as unknown as ArxivSearchParams);
          return result as any;
        } else if (name === 'get_arxiv_paper') {
          const paperId = (args as any)?.paperId as string;
          const result = await this.getArxivPaper(paperId);
          return result as any;
        } else {
          throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${errorMessage}`,
            },
          ],
        } as any;
      }
    });
  }

  private async searchArxiv(params: ArxivSearchParams) {
    const { query, maxResults = 10, sortBy = 'relevance' } = params;

    const searchQuery = query.replace(/\s+/g, '+');
    const sortOrder = sortBy === 'relevance' ? 'relevance' : 'lastUpdatedDate';
    const url = `http://export.arxiv.org/api/query?search_query=all:${searchQuery}&start=0&max_results=${maxResults}&sortBy=${sortOrder}&sortOrder=descending`;

    const response = await fetch(url);
    const xmlData = await response.text();

    return new Promise((resolve, reject) => {
      parseString(xmlData, (err: any, result: any) => {
        if (err) {
          reject(err);
          return;
        }

        const entries = result.feed.entry || [];
        const papers = entries.map((entry: any) => ({
          id: entry.id[0],
          title: entry.title[0].trim(),
          authors: entry.author?.map((a: any) => a.name[0]).join(', ') || '',
          summary: entry.summary[0].trim(),
          published: entry.published[0],
          updated: entry.updated[0],
          pdfUrl: entry.link?.find((l: any) => l.$.title === 'pdf')?.$?.href,
          categories: entry.category?.map((c: any) => c.$.term).join(', ') || '',
        }));

        resolve({
          content: [
            {
              type: 'text',
              text: JSON.stringify(papers, null, 2),
            },
          ],
        });
      });
    });
  }

  private async getArxivPaper(paperId: string) {
    const url = `http://export.arxiv.org/api/query?id_list=${paperId}`;
    
    const response = await fetch(url);
    const xmlData = await response.text();

    return new Promise((resolve, reject) => {
      parseString(xmlData, (err: any, result: any) => {
        if (err) {
          reject(err);
          return;
        }

        const entries = result.feed.entry;
        if (!entries || entries.length === 0) {
          reject(new Error(`Paper ${paperId} not found`));
          return;
        }

        const paper = entries[0];
        const details = {
          id: paper.id[0],
          title: paper.title[0].trim(),
          authors: paper.author?.map((a: any) => a.name[0]) || [],
          summary: paper.summary[0].trim(),
          published: paper.published[0],
          updated: paper.updated[0],
          pdfUrl: paper.link?.find((l: any) => l.$.title === 'pdf')?.$?.href,
          categories: paper.category?.map((c: any) => c.$.term) || [],
          comment: paper.comment?.[0] || '',
          doi: paper['arxiv:doi']?.[0] || '',
        };

        resolve({
          content: [
            {
              type: 'text',
              text: JSON.stringify(details, null, 2),
            },
          ],
        });
      });
    });
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('arXiv MCP Server running on stdio');
  }
}

const server = new ArxivServer();
server.run().catch(console.error);

