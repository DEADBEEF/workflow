package edu.workflow.server;

import java.sql.SQLException;
import java.util.Collection;
import java.util.concurrent.Executors;

import org.jboss.netty.channel.socket.nio.NioServerSocketChannelFactory;

import com.googlecode.protobuf.pro.duplex.PeerInfo;
import com.googlecode.protobuf.pro.duplex.execute.RpcServerCallExecutor;
import com.googlecode.protobuf.pro.duplex.execute.ThreadPoolCallExecutor;
import com.googlecode.protobuf.pro.duplex.server.DuplexTcpServerBootstrap;

import edu.workflow.server.database.Database;
import edu.workflow.server.services.JobServiceImpl;

public class Server {
	private static final int port = 8081;
	private static final String databaseHost = "127.0.0.1";
	private static final String databaseUser = "server_user";
	private static final String databasePassword = "server101";
	private static final String databaseWork = "workflow";
	private Database database;
	
	public Server() {
		try {
			database = new Database(databaseHost, databaseUser, 
					databasePassword, databaseWork);
			
		} catch (SQLException e) {
        	e.printStackTrace();
        	System.out.println("It broke");
        } catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		PeerInfo serverInfo = new PeerInfo("serverHostname", port);
		RpcServerCallExecutor executor = new ThreadPoolCallExecutor(20, 20);
		DuplexTcpServerBootstrap bootstrap = new DuplexTcpServerBootstrap(
                serverInfo,
        new NioServerSocketChannelFactory(
                Executors.newCachedThreadPool(),
                Executors.newCachedThreadPool()),
        executor);
		bootstrap.getRpcServiceRegistry().registerService(new JobServiceImpl(database));
        bootstrap.bind();
	}

}
