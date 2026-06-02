# Copy plugins from 1 vault to another using obsidian CLI
obsidian vault="Source Vault" plugins filter=community > plugins_to_install.txt
xargs -I {} obsidian vault="dest vault" plugin:install id={} < plugins_to_install.txt
 
cp "/path/to/source-vault/.obsidian/community-plugins.json" "/path/to/dest-vault/.obsidian/" 
