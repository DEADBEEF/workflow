package edu.workflow.server.services;

import java.sql.SQLException;

import com.google.protobuf.RpcCallback;
import com.google.protobuf.RpcController;

import edu.workflow.ping.PingPong.Job;
import edu.workflow.ping.PingPong.JobService;
import edu.workflow.ping.PingPong.JobStatus;
import edu.workflow.ping.PingPong.JobStatusEnum;
import edu.workflow.ping.PingPong.JobType;
import edu.workflow.ping.PingPong.Response;
import edu.workflow.ping.PingPong.ResponseEnum;
import edu.workflow.ping.PingPong.StringMessage;
import edu.workflow.server.database.Database;

public class JobServiceImpl extends JobService {
	private Database database;
	public JobServiceImpl(Database database) {
		this.database = database;
	}
	
	@Override
	public void addJob(RpcController controller, Job request,
			RpcCallback<Response> done)  {
		
		String jobId = request.getName();
		JobType type = request.getType();
		String asignee = request.getAssignee();
		Response.Builder responseBuilder = Response.newBuilder();
		try {
			if (!database.checkJobExists(jobId)){
				database.addJob(jobId, type, asignee);
				responseBuilder.setCode(ResponseEnum.NOERROR);
			} else {
				responseBuilder.setCode(ResponseEnum.JOB_EXISTS);
			}
		} catch (SQLException e) {
			e.printStackTrace();
			responseBuilder.setCode(ResponseEnum.UNKNOWN_ERROR);
		}

		done.run(responseBuilder.build());

	}

	@Override
	public void checkJobStatus(RpcController controller, StringMessage request,
			RpcCallback<JobStatus> done) {
		String jobId = request.getValue();
		JobStatus.Builder statusBuilder = JobStatus.newBuilder();
		try {
			JobStatusEnum status = database.checkStatus(jobId);
			statusBuilder.setStatus(status);
			
		} catch (SQLException e) {
			e.printStackTrace();
			statusBuilder.setStatus(JobStatusEnum.JOBNOTFOUND);
		}
		done.run(statusBuilder.build());
	}

}
