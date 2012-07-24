package edu.workflow.server.services;

import com.google.protobuf.RpcCallback;
import com.google.protobuf.RpcController;

import edu.workflow.ping.PingPong.Ping;
import edu.workflow.ping.PingPong.PingPongService;
import edu.workflow.ping.PingPong.Pong;

public class PingPongServiceImpl extends PingPongService {

	@Override
	public void ping(RpcController controller, Ping request,
			RpcCallback<Pong> done) {
		Pong pong = Pong.newBuilder().setPongData(request.getPingData()).build();
		done.run(pong);
	}

	@Override
	public void fail(RpcController controller, Ping request,
			RpcCallback<Pong> done) {
		// TODO Auto-generated method stub

	}

}
