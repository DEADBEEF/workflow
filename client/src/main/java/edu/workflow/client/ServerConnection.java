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
import edu.workflow.ping.PingPong.JobStatus;
import edu.workflow.ping.PingPong.Response;
import edu.workflow.ping.PingPong.StringMessage;

public class ServerConnection {
	private static final String serverHost = "localhost";
	private static final int port = 8081;
	private RpcClientChannel channel;
	private DuplexTcpClientBootstrap bootstrap;
	private JobService.BlockingInterface jobService;
	private RpcController controller;
	
	public ServerConnection(String clientName) throws IOException {
		PeerInfo client = new PeerInfo("120.0.0.1",1234);
    	PeerInfo serverInfo = new PeerInfo(serverHost, port);
    	ThreadPoolCallExecutor executor = new ThreadPoolCallExecutor(1, 2);
    	
    	bootstrap = new DuplexTcpClientBootstrap(
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
         channel = bootstrap.peerWith(serverInfo);
         bootstrap.setOption("connectTimeoutMillis",10000);
         bootstrap.setOption("connectResponseTimeoutMillis",10000);
         bootstrap.setOption("receiveBufferSize", 1048576);
         bootstrap.setOption("tcpNoDelay", false);
         jobService = JobService.newBlockingStub(channel);
         controller = channel.newRpcController();

	}
	
	public void close() {
		channel.close();
		bootstrap.releaseExternalResources();
	}
	
	public Response addJob(Job job) throws ServiceException {
        Response status = jobService.addJob(controller, job); 
        return status;
	}
	
	public JobStatus checkJobStatus(StringMessage jobID) throws ServiceException {
		return jobService.checkJobStatus(controller, jobID);
	}
	

}
