https://www.youtube.com/watch?v=Y_Rk6QgWUbE
Learn how to build an MCP Server in Java

GitHub Repo: https://github.com/danvega/javaone-mcp
MCP Inspector tool: https://www.npmjs.com/package/mcp-inspector
Java SDK documentation: https://java.sdk.modelcontextprotocol.io/latest/
https://github.com/modelcontextprotocol/java-sdk

also debug it while developing. Just add environment variable in MCP inspector:
JAVA_TOOL_OPTIONS = -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005
and configure IntelliJ IDEA with a "Remote JVM Debug" run configuration.
