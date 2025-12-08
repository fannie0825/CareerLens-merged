/**
 * Security Check Script
 * Verifies that API keys are not exposed in the repository
 * Run with: node scripts/check-security.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔒 CareerLens Security Check\n');
console.log('='.repeat(50) + '\n');

let hasIssues = false;

// 1. Check if .env is in .gitignore
console.log('1️⃣  Checking .gitignore...');
const gitignorePath = path.join(process.cwd(), '.gitignore');
if (fs.existsSync(gitignorePath)) {
  const gitignoreContent = fs.readFileSync(gitignorePath, 'utf8');
  if (gitignoreContent.includes('.env')) {
    console.log('   ✅ .env is in .gitignore\n');
  } else {
    console.log('   ❌ .env is NOT in .gitignore!\n');
    hasIssues = true;
  }
} else {
  console.log('   ⚠️  .gitignore file not found\n');
  hasIssues = true;
}

// 2. Check if .env is tracked by git
console.log('2️⃣  Checking if .env is tracked by git...');
try {
  const trackedFiles = execSync('git ls-files', { encoding: 'utf8' });
  if (trackedFiles.includes('.env')) {
    console.log('   ❌ .env IS tracked by git! This is a security risk!\n');
    console.log('   🔧 Fix: Run "git rm --cached .env" and commit\n');
    hasIssues = true;
  } else {
    console.log('   ✅ .env is NOT tracked by git\n');
  }
} catch (error) {
  console.log('   ⚠️  Could not check git status (not a git repo?)\n');
}

// 3. Check if .env exists locally
console.log('3️⃣  Checking for .env file...');
const envPath = path.join(process.cwd(), '.env');
if (fs.existsSync(envPath)) {
  console.log('   ✅ .env file exists locally\n');
  
  // Check if it contains placeholder values
  const envContent = fs.readFileSync(envPath, 'utf8');
  const hasPlaceholders = envContent.includes('your-') || 
                         envContent.includes('here') ||
                         envContent.includes('placeholder');
  
  if (hasPlaceholders) {
    console.log('   ⚠️  .env contains placeholder values\n');
    console.log('   💡 Make sure to replace with actual API keys\n');
  } else {
    console.log('   ✅ .env appears to have real values configured\n');
  }
} else {
  console.log('   ⚠️  .env file not found\n');
  console.log('   💡 Create .env from .env.example\n');
}

// 4. Check for hardcoded keys in source code
console.log('4️⃣  Checking for hardcoded API keys in source code...');
try {
  const sourceFiles = execSync('find . -type f -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v ".git"', { encoding: 'utf8' });
  const files = sourceFiles.trim().split('\n').filter(f => f);
  
  let foundHardcoded = false;
  for (const file of files) {
    try {
      const content = fs.readFileSync(file, 'utf8');
      // Look for patterns that might be hardcoded keys
      const suspiciousPatterns = [
        /api[_-]?key\s*[:=]\s*["']([^"']{20,})["']/i,
        /api[_-]?key\s*[:=]\s*`([^`]{20,})`/i,
      ];
      
      for (const pattern of suspiciousPatterns) {
        if (pattern.test(content)) {
          console.log(`   ⚠️  Potential hardcoded key found in: ${file}\n`);
          foundHardcoded = true;
          hasIssues = true;
        }
      }
    } catch (err) {
      // Skip files that can't be read
    }
  }
  
  if (!foundHardcoded) {
    console.log('   ✅ No hardcoded API keys found in source code\n');
  }
} catch (error) {
  console.log('   ⚠️  Could not scan source files\n');
}

// 5. Check .env.example
console.log('5️⃣  Checking .env.example...');
const envExamplePath = path.join(process.cwd(), '.env.example');
if (fs.existsSync(envExamplePath)) {
  const exampleContent = fs.readFileSync(envExamplePath, 'utf8');
  if (exampleContent.includes('your-') || exampleContent.includes('here')) {
    console.log('   ✅ .env.example contains placeholders (safe to commit)\n');
  } else {
    console.log('   ⚠️  .env.example might contain real keys!\n');
    hasIssues = true;
  }
} else {
  console.log('   ⚠️  .env.example not found\n');
}

// Summary
console.log('='.repeat(50));
if (hasIssues) {
  console.log('\n❌ Security issues found! Please review above.\n');
  console.log('📖 See SECURITY_GUIDE.md for how to fix issues.\n');
  process.exit(1);
} else {
  console.log('\n✅ Security check passed! Your API keys are protected.\n');
  console.log('💡 Remember: Never commit .env files!\n');
  process.exit(0);
}
