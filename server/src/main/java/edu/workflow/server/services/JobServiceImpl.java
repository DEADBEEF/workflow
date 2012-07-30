package edu.workflow.server.services;

import com.google.protobuf.RpcCallback;
import com.google.protobuf.RpcController;

import edu.workflow.ping.PingPong.Job;
import edu.workflow.ping.PingPong.JobService;
import edu.workflow.ping.PingPong.Pong;
import edu.workflow.ping.PingPong.Response;
import edu.workflow.ping.PingPong.ResponseEnum;

public class JobServiceImpl extends JobService {

	@Override
	public void addJob(RpcController controller, Job request,
			RpcCallback<Response> done) {
		// TODO Auto-generated method stub
		Response response =  Response.newBuilder()
				.setCode(ResponseEnum.NOERROR).build();
		//pong = Pong.newBuilder().setPongData(request.getPingData()).build();
		
		done.run(response);

	}

}
