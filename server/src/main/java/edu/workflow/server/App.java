package edu.workflow.server;



import java.sql.SQLException;
import java.util.concurrent.Executors;

import org.jboss.netty.channel.socket.nio.NioServerSocketChannelFactory;

import com.googlecode.protobuf.pro.duplex.PeerInfo;
import com.googlecode.protobuf.pro.duplex.execute.RpcServerCallExecutor;
import com.googlecode.protobuf.pro.duplex.execute.ThreadPoolCallExecutor;
import com.googlecode.protobuf.pro.duplex.server.DuplexTcpServerBootstrap;

import edu.workflow.ping.PingPong;
import edu.workflow.ping.PingPong.Ping;
import edu.workflow.server.database.Database;
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
        bootstrap.getRpcServiceRegistry().registerService(new PingPongServiceImpl());
        bootstrap.bind();
        try {
        	Database db = new Database("localhost", "server_user", "server101", "workflow");
        	db.addUser("michiel");
        } catch (SQLException e) {
        	
        } catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
}
