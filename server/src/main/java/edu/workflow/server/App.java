package edu.workflow.server;



import java.sql.SQLException;
import java.util.Collection;
import java.util.concurrent.Executors;

import org.jboss.netty.channel.socket.nio.NioServerSocketChannelFactory;

import com.googlecode.protobuf.pro.duplex.PeerInfo;
import com.googlecode.protobuf.pro.duplex.execute.RpcServerCallExecutor;
import com.googlecode.protobuf.pro.duplex.execute.ThreadPoolCallExecutor;
import com.googlecode.protobuf.pro.duplex.server.DuplexTcpServerBootstrap;

import edu.workflow.ping.PingPong;
import edu.workflow.ping.PingPong.Ping;
import edu.workflow.server.database.Database;
import edu.workflow.server.services.JobServiceImpl;
import edu.workflow.server.services.PingPongServiceImpl;


/**
 * Hello world!
 *
 */
public class App
{
    public static void main( String[] args )
    {
 
    	PeerInfo serverInfo = new PeerInfo("serverHostname", 8081);
        System.out.println( "Hello World!" );
        RpcServerCallExecutor executor = new ThreadPoolCallExecutor(10, 10);
        
        DuplexTcpServerBootstrap bootstrap = new DuplexTcpServerBootstrap(
                        serverInfo,
                new NioServerSocketChannelFactory(
                        Executors.newCachedThreadPool(),
                        Executors.newCachedThreadPool()),
                executor);
        bootstrap.getRpcServiceRegistry().registerService(new JobServiceImpl());
        bootstrap.bind();
        try {
        	Database db = new Database("localhost", "server_user", "server101", "workflow");
        	Collection<String> users = db.getUsers();
        	for (String user :users) {
        		System.out.println(user);
        	}
        } catch (SQLException e) {
        	e.printStackTrace();
        	System.out.println("It broke");
        } catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
}
