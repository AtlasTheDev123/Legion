import * as vscode from 'vscode';
import { LegionClient } from './client';
import { CodeCompletionProvider } from './providers/completionProvider';
import { ChatProvider } from './providers/chatProvider';
import { CodeLensProvider } from './providers/codeLensProvider';

let legionClient: LegionClient;
let completionProvider: CodeCompletionProvider;
let chatProvider: ChatProvider;

export async function activate(context: vscode.ExtensionContext) {
    console.log('Legion Copilot extension is now active!');

    // Initialize Legion client
    const config = vscode.workspace.getConfiguration('legion');
    const apiEndpoint = config.get<string>('apiEndpoint') || 'http://localhost:8000';
    const authToken = config.get<string>('authToken') || '';

    legionClient = new LegionClient(apiEndpoint, authToken);

    // Initialize providers
    completionProvider = new CodeCompletionProvider(legionClient);
    chatProvider = new ChatProvider(legionClient, context);

    // Register providers
    const completionDisposable = vscode.languages.registerInlineCompletionItemProvider(
        { pattern: '**' },
        completionProvider
    );

    // Register code lens provider
    const codeLensDisposable = vscode.languages.registerCodeLensProvider(
        { pattern: '**' },
        new CodeLensProvider(legionClient)
    );

    // Register chat sidebar
    chatProvider.registerSidebar(context);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('legion.generateCode', () => handleGenerateCode(legionClient)),
        vscode.commands.registerCommand('legion.refactorCode', () => handleRefactorCode(legionClient)),
        vscode.commands.registerCommand('legion.explainCode', () => handleExplainCode(legionClient)),
        vscode.commands.registerCommand('legion.generateTests', () => handleGenerateTests(legionClient)),
        vscode.commands.registerCommand('legion.fixErrors', () => handleFixErrors(legionClient)),
        vscode.commands.registerCommand('legion.optimizeCode', () => handleOptimizeCode(legionClient)),
        vscode.commands.registerCommand('legion.securityAudit', () => handleSecurityAudit(legionClient)),
        vscode.commands.registerCommand('legion.chat', () => chatProvider.openChat(context)),
        completionDisposable,
        codeLensDisposable
    );

    // Monitor file changes
    const fileWatcher = vscode.workspace.createFileSystemWatcher('**/*.{js,ts,py,java,go}');
    fileWatcher.onDidChange(() => completionProvider.invalidateCache());
    context.subscriptions.push(fileWatcher);
}

async function handleGenerateCode(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const prompt = await vscode.window.showInputBox({
        prompt: 'Describe the code you want to generate',
        placeHolder: 'e.g., REST API endpoint for user management'
    });

    if (!prompt) return;

    const language = editor.document.languageId;
    const code = await client.generateCode(prompt, language);

    const selection = editor.selection;
    editor.edit(editBuilder => {
        editBuilder.replace(selection, code);
    });

    vscode.window.showInformationMessage('Code generated successfully!');
}

async function handleRefactorCode(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const selectedText = editor.document.getText(editor.selection);
    if (!selectedText) {
        vscode.window.showWarningMessage('Please select code to refactor');
        return;
    }

    const refactored = await client.refactorCode(selectedText);

    editor.edit(editBuilder => {
        editBuilder.replace(editor.selection, refactored);
    });

    vscode.window.showInformationMessage('Code refactored successfully!');
}

async function handleExplainCode(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const selectedText = editor.document.getText(editor.selection);
    if (!selectedText) {
        vscode.window.showWarningMessage('Please select code to explain');
        return;
    }

    const explanation = await client.explainCode(selectedText);
    vscode.window.showInformationMessage(`Explanation:\n${explanation}`);
}

async function handleGenerateTests(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const selectedText = editor.document.getText(editor.selection);
    const tests = await client.generateTests(selectedText, editor.document.languageId);

    const newEditor = await vscode.workspace.openTextDocument({
        language: editor.document.languageId,
        content: tests
    });

    vscode.window.showTextDocument(newEditor);
}

async function handleFixErrors(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const diagnostics = vscode.languages.getDiagnostics(editor.document.uri);
    if (diagnostics.length === 0) {
        vscode.window.showInformationMessage('No errors found');
        return;
    }

    const errors = diagnostics.map(d => d.message).join('\n');
    const fixed = await client.fixErrors(editor.document.getText(), errors);

    editor.edit(editBuilder => {
        const fullRange = new vscode.Range(
            editor.document.positionAt(0),
            editor.document.positionAt(editor.document.getText().length)
        );
        editBuilder.replace(fullRange, fixed);
    });
}

async function handleOptimizeCode(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const code = editor.document.getText();
    const optimized = await client.optimizeCode(code, editor.document.languageId);

    editor.edit(editBuilder => {
        const fullRange = new vscode.Range(
            editor.document.positionAt(0),
            editor.document.positionAt(code.length)
        );
        editBuilder.replace(fullRange, optimized);
    });
}

async function handleSecurityAudit(client: LegionClient) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const results = await client.securityAudit(editor.document.uri.fsPath);
    
    const panel = vscode.window.createWebviewPanel(
        'legionSecurityAudit',
        'Legion Security Audit',
        vscode.ViewColumn.Beside
    );

    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: sans-serif; margin: 20px; }
                .vulnerability { 
                    border-left: 4px solid #f44747; 
                    padding: 10px; 
                    margin: 10px 0;
                    background: #f4474715;
                }
                .critical { border-left-color: #f44747; }
                .high { border-left-color: #ce9178; }
                .medium { border-left-color: #d7ba7d; }
                .low { border-left-color: #6a9955; }
            </style>
        </head>
        <body>
            <h2>Security Audit Results</h2>
            ${results.map(vuln => `
                <div class="vulnerability ${vuln.severity}">
                    <strong>${vuln.title}</strong> (${vuln.severity})
                    <p>${vuln.description}</p>
                    <code>${vuln.location}</code>
                </div>
            `).join('')}
        </body>
        </html>
    `;
}

export function deactivate() {
    console.log('Legion Copilot extension deactivated');
}
