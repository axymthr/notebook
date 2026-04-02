package org.axymthr;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.modelcontextprotocol.json.McpJsonMapper;
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.McpServerFeatures;
import io.modelcontextprotocol.server.McpSyncServer;
import io.modelcontextprotocol.server.transport.StdioServerTransportProvider;
import io.modelcontextprotocol.spec.McpSchema;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class Main {

    private static final Logger log = LoggerFactory.getLogger(Main.class);
    private static PresentationTools presentationTools = new PresentationTools();

    public static void main(String[] args) {
        //Stdio server transport
        var transportProvider = new StdioServerTransportProvider(McpJsonMapper.createDefault());

        // sync tool spec
        var syncToolSpecification = getSyncToolSpecification();

        McpSyncServer mcpSyncServer = McpServer.sync(transportProvider)
                .serverInfo("mcp-server", "0.0.1")
                .capabilities(McpSchema.ServerCapabilities.builder()
                        .tools(true)
                        .logging()
                        .build())
                .tools(syncToolSpecification)
                .build();

        log.info("Starting MCP server...");
    }

    private static McpServerFeatures.SyncToolSpecification getSyncToolSpecification() {
        var schema = """
                {
                    "type": "object",
                    "id": "urn:jsonschema:Operation",
                    "properties": {
                        "operation": {
                            "type": "string"
                        }
                    }
                }
                """;
        var syncToolSpecification = new McpServerFeatures.SyncToolSpecification(
                new McpSchema.Tool("get presentations", "Get a list of all presentations", schema),
                (exchange, arguments) -> {
                    List<Presentation> presentations = presentationTools.getPresentations();
                    List<McpSchema.Content> contents = new ArrayList<>();
                    for (Presentation presentation : presentations) {
                        contents.add(new McpSchema.TextContent(presentation.toString()));
                    }
                    return new McpSchema.CallToolResult(contents, false);
                }
        );
        return syncToolSpecification;
    }
}
