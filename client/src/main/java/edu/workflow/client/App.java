package edu.workflow.client;

import java.io.IOException;
import java.util.concurrent.Executors;

import org.jboss.netty.channel.socket.nio.NioClientSocketChannelFactory;

import com.google.protobuf.ByteString;
import com.google.protobuf.RpcController;
import com.google.protobuf.ServiceException;
import com.googlecode.protobuf.pro.duplex.PeerInfo;
import com.googlecode.protobuf.pro.duplex.RpcClientChannel;
import com.googlecode.protobuf.pro.duplex.client.DuplexTcpClientBootstrap;
import com.googlecode.protobuf.pro.duplex.execute.ThreadPoolCallExecutor;

import edu.workflow.ping.PingPong.Ping;
import edu.workflow.ping.PingPong.PingPongService;
import edu.workflow.ping.PingPong.PingPongService.BlockingInterface;
import edu.workflow.ping.PingPong.Pong;

/**
 * Hello world!
 *
 */
public class App
{
    public static void main( String[] args ) throws IOException, ServiceException
    {
    	PeerInfo client = new PeerInfo("127.0.0.1",1234);
    	PeerInfo serverInfo = new PeerInfo("127.0.0.1",8081);
    	ThreadPoolCallExecutor executor = new ThreadPoolCallExecutor(3, 10);
    	 DuplexTcpClientBootstrap bootstrap = new DuplexTcpClientBootstrap(
                 client, 
                 new NioClientSocketChannelFactory(
         Executors.newCachedThreadPool(),
         Executors.newCachedThreadPool()),
         executor);
    	 bootstrap.setCompression(true);
    	 bootstrap.setOption("connectTimeoutMillis",10000);
         bootstrap.setOption("connectResponseTimeoutMillis",10000);
         bootstrap.setOption("receiveBufferSize", 1048576);
         bootstrap.setOption("tcpNoDelay", false);
         RpcClientChannel channel = bootstrap.peerWith(serverInfo);
         bootstrap.setOption("connectTimeoutMillis",10000);
         bootstrap.setOption("connectResponseTimeoutMillis",10000);
         bootstrap.setOption("receiveBufferSize", 1048576);
         bootstrap.setOption("tcpNoDelay", false);
         
         BlockingInterface pingpongService = PingPongService.newBlockingStub(channel);
         RpcController controller = channel.newRpcController();
                         
         Ping request = Ping.newBuilder().setPongDataLength(4)
        		 .setProcessingTime(50)
        		 .setPingData(ByteString.copyFromUtf8("test"))
        		 .build();
         Pong pong = pingpongService.ping(controller, request);
         
         
        System.out.println( "Hello World!" );
    }
}
