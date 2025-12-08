/**
 * Script to check if environment variables are set correctly
 * Run with: node scripts/check-env.js
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Checking CareerLens API Configuration...\n');

// Check if .env file exists
const envPath = path.join(process.cwd(), '.env');
const envExamplePath = path.join(process.cwd(), '.env.example');

if (!fs.existsSync(envPath)) {
  console.log('❌ .env file not found!');
  console.log('📝 Creating .env from .env.example...\n');
  
  if (fs.existsSync(envExamplePath)) {
    fs.copyFileSync(envExamplePath, envPath);
    console.log('✅ Created .env file');
    console.log('⚠️  Please edit .env and add your API keys!\n');
  } else {
    console.log('❌ .env.example not found either!');
    process.exit(1);
  }
} else {
  console.log('✅ .env file exists');
}

// Read .env file
const envContent = fs.readFileSync(envPath, 'utf8');
const lines = envContent.split('\n');

console.log('\n📋 Current Configuration:\n');

const requiredVars = [
  'REACT_APP_API_URL',
  'REACT_APP_USE_MOCK_API',
];

const optionalVars = [
  'REACT_APP_AZURE_OPENAI_API_KEY',
  'REACT_APP_AZURE_OPENAI_ENDPOINT',
  'REACT_APP_RAPIDAPI_KEY',
  'REACT_APP_BACKEND_API_KEY',
];

let hasErrors = false;

// Check required variables
console.log('Required Variables:');
requiredVars.forEach(varName => {
  const found = lines.some(line => line.trim().startsWith(varName + '='));
  if (found) {
    const line = lines.find(l => l.trim().startsWith(varName + '='));
    const value = line.split('=')[1]?.trim();
    if (value && !value.includes('your-') && !value.includes('here')) {
      console.log(`  ✅ ${varName} = ${value.substring(0, 20)}...`);
    } else {
      console.log(`  ⚠️  ${varName} = (not configured)`);
    }
  } else {
    console.log(`  ❌ ${varName} = (missing)`);
    hasErrors = true;
  }
});

// Check optional variables
console.log('\nOptional Variables (API Keys):');
optionalVars.forEach(varName => {
  const found = lines.some(line => line.trim().startsWith(varName + '='));
  if (found) {
    const line = lines.find(l => l.trim().startsWith(varName + '='));
    const value = line.split('=')[1]?.trim();
    if (value && !value.includes('your-') && !value.includes('here')) {
      const masked = value.substring(0, 8) + '...' + value.substring(value.length - 4);
      console.log(`  ✅ ${varName} = ${masked}`);
    } else {
      console.log(`  ⚠️  ${varName} = (not configured)`);
    }
  } else {
    console.log(`  ⚠️  ${varName} = (not set - optional)`);
  }
});

// Check for mock API mode
const useMock = lines.find(l => l.includes('REACT_APP_USE_MOCK_API'));
if (useMock && useMock.includes('true')) {
  console.log('\n💡 Mock API mode is enabled - no real API keys needed');
} else {
  console.log('\n💡 Real API mode - ensure API keys are configured');
}

console.log('\n' + '='.repeat(50));
if (hasErrors) {
  console.log('❌ Some required variables are missing!');
  console.log('📝 Please edit .env file and add missing variables.\n');
  process.exit(1);
} else {
  console.log('✅ Configuration looks good!\n');
  process.exit(0);
}
