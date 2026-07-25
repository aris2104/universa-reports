#!/usr/bin/env node

const { spawnSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Couleurs ANSI pour le terminal
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

/**
 * Détecte la commande Python 3 disponible sur la machine.
 * Supporte 'python3', 'python' et le lanceur Windows 'py -3'.
 */
function getPythonCommand() {
  const candidates = [
    { name: 'python3', versionArgs: ['--version'], runArgs: [] },
    { name: 'python', versionArgs: ['--version'], runArgs: [] },
    { name: 'py', versionArgs: ['-3', '--version'], runArgs: ['-3'] }
  ];

  for (const candidate of candidates) {
    const result = spawnSync(candidate.name, candidate.versionArgs, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe']
    });

    if (result.error || result.status !== 0) {
      continue;
    }

    const output = (result.stdout || result.stderr || '').trim();
    const match = /Python\s+(\d+)\./i.exec(output);
    if (match && Number(match[1]) >= 3) {
      return candidate;
    }
  }

  return null;
}

const pythonCommand = getPythonCommand();

// 1. Vérification de l'existence de Python 3
if (!pythonCommand) {
  console.error(`\n${RED}✘ Erreur : Python 3 n'a pas été détecté sur votre système.${RESET}`);
  console.error(`${YELLOW}universa-reports nécessite Python 3 pour fonctionner.${RESET}\n`);
  console.log(`Veuillez installer Python depuis : ${GREEN}https://www.python.org/downloads/${RESET}\n`);
  process.exit(1);
}

// 2. Vérification de l'existence de cli.py
const cliPath = path.resolve(__dirname, '..', 'python-src', 'cli.py');
if (!fs.existsSync(cliPath)) {
  console.error(`${RED}✘ Erreur : Impossible de trouver le fichier CLI Python à l'emplacement attendu :${RESET}`);
  console.error(`${YELLOW}${cliPath}${RESET}`);
  process.exit(1);
}

// 3. Lancement interactif du script Python
const child = spawn(pythonCommand.name, [...pythonCommand.runArgs, cliPath], {
  stdio: 'inherit'
});

child.on('error', (err) => {
  console.error(`${RED}Erreur lors du lancement du script Python :${RESET}`, err.message);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code === null ? 1 : code);
});