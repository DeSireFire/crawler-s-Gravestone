import TurndownService from 'turndown';

// 创建一个新的TurndownService实例
const turndownService = new TurndownService();

export function convertHtmlToMarkdown(html) {
    return turndownService.turndown(html);
}
