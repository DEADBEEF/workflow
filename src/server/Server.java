package server;

import java.util.concurrent.Executors;

import com.googlecode.protobuf.socketrpc.RpcServer;
import com.googlecode.protobuf.socketrpc.ServerRpcConnectionFactory;
import com.googlecode.protobuf.socketrpc.SocketRpcConnectionFactories;

public class Server {
	private static final int threadPoolSize = 4;
	private static final int port = 8888;
	
	public static void main(String [] args) {
		// Start server
		ServerRpcConnectionFactory rpcConnectionFactory = SocketRpcConnectionFactories
		    .createServerRpcConnectionFactory(port);
		RpcServer server = new RpcServer(rpcConnectionFactory, 
		    Executors.newFixedThreadPool(threadPoolSize), true);
		server.registerService(new MyServiceImpl()); // For non-blocking impl
		server.registerBlockingService(MyService
		    .newReflectiveBlockingService(new MyBlockingInterfaceImpl())); // For blocking impl
		server.run();
	}
}
