package edu.workflow.client;

import java.io.IOException;
import java.util.concurrent.Executors;

import org.jboss.netty.channel.socket.nio.NioClientSocketChannelFactory;

import com.google.protobuf.RpcController;
import com.google.protobuf.ServiceException;
import com.googlecode.protobuf.pro.duplex.PeerInfo;
import com.googlecode.protobuf.pro.duplex.RpcClientChannel;
import com.googlecode.protobuf.pro.duplex.client.DuplexTcpClientBootstrap;
import com.googlecode.protobuf.pro.duplex.execute.ThreadPoolCallExecutor;

import edu.workflow.ping.PingPong.Job;
import edu.workflow.ping.PingPong.JobService;
import edu.workflow.ping.PingPong.JobType;
import edu.workflow.ping.PingPong.Response;
import edu.workflow.ping.PingPong.ResponseEnum;

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
    	ThreadPoolCallExecutor executor = new ThreadPoolCallExecutor(1, 2);
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
         
         JobService.BlockingInterface jobService = JobService.newBlockingStub(channel);
         RpcController controller = channel.newRpcController();
        
         Job job = Job.newBuilder()
        		 .setName("Test Job")
        		 .setAssignee("Michiel")
        		 .setType(JobType.CLEAN).build();

         Response status = jobService.addJob(controller, job);
         if (status.getCode() == ResponseEnum.NOERROR) {
        	 System.out.println("SUCCESS");
         }
         channel.close();
         bootstrap.releaseExternalResources();
    }
}
