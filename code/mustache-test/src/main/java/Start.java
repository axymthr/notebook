import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.eclipse.jetty.server.Connector;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.bio.SocketConnector;
import org.eclipse.jetty.webapp.WebAppContext;
import org.springframework.context.ApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

public class Start {
	// the only way to catch and throw exceptions during startup is to intercept
	// the call chain and collect them:
	protected final transient List<Exception> startupExceptions = Collections
			.synchronizedList(new ArrayList<Exception>());
	private ApplicationContext applicationContext;

	public static void main(String[] args) {
		Start start = new Start();
		start.startServer(8080);
	}

	public Server startServer(int port) {
		Server server = new Server();
		Connector connector = new SocketConnector();
		connector.setResponseBufferSize(10000000);
		connector.setPort(port);
		connector.setServer(server);
		
		server.setConnectors(new Connector[] { connector });
		WebAppContext webContext = createWebappContextHandler();
		server.setHandler(webContext);
		try {
			startupExceptions.clear();
			server.start();
			if (startupExceptions.size() > 0) {
				Exception exception = startupExceptions.get(0);
				throw new RuntimeException( "Errors during startup. The first is "
								+ exception.getClass().getName() + ": " + exception.getMessage(), exception);
			}
			String serverName = server.getConnectors()[0].getName();
			if (serverName.startsWith("0.0.0.0")) {
				serverName = serverName.replace("0.0.0.0", "localhost");
			}
			System.out.println("Server started on http://" + serverName + "/mustache/index.html");
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(-1);
		}
		applicationContext = WebApplicationContextUtils.getWebApplicationContext(webContext.getServletContext());
		return server;
	}

	private WebAppContext createWebappContextHandler() {
		WebAppContext context = new WebAppContext("src/main/webapp", "/mustache") {
			@Override
			protected void startContext() throws Exception {
				try {
					super.startContext();
				} catch (Exception exception) {
					addStartupException(exception);
					throw exception;
				}
			}
		};
		return context;
	}

	private void addStartupException(Exception e) {
		startupExceptions.add(e);
	}

	public ApplicationContext getApplicationContext() {
		return applicationContext;
	}
}
