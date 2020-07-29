<template>
    <div class="fillcontain">
        <div>
            <el-form :inline="true" ref="add_data" >
                <el-form-item label="根据时间筛选:">
                    <el-date-picker v-model="search_data.startTime" type="datetime" placeholder="选择开始时间"></el-date-picker>--
                    <el-date-picker v-model="search_data.endTime" type="datetime" placeholder="选择结束时间"></el-date-picker>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" size="small" icon="search" @click="onScreeoutMoney()">筛选</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="table_container">
            <el-table
            v-if="tableData.length > 0"
            :data="tableData"
            max-height="450"
            border
            :default-sort="{prop: 'id', order: 'descending'}"
            style="width: 100%"
            >
                <el-table-column prop="id" label="序号" align="center" width="100"></el-table-column>
                <el-table-column prop="timestamp" label="创建时间" align="center" width="200" sortable>
                <template slot-scope="scope">
                    <el-icon name="time"></el-icon>
                    <span style="margin-left: 10px">{{ time(scope.row.timestamp)}}</span>
                </template>
                </el-table-column>
                <el-table-column prop="hostname" label="服务器主机" align="center" width="150"></el-table-column>
                <el-table-column prop="name" label="报警来源" align="center" width="300"></el-table-column>
                <el-table-column prop="level" label="危险级别" align="center" width="90"></el-table-column>
                <el-table-column prop="operation" align="center" label="操作" fixed="right" width="240">
                  <template slot-scope="scope">
                    <el-button type="warning" icon="edit" size="small"
                    @click="showDetail(scope.$index,scope.row)">详情</el-button>
                    <el-button type="danger" icon="delete" size="small"
                    @click="onDelete(scope.$index,scope.row)">删除</el-button>
                </template>
                </el-table-column>
            </el-table>
            <!-- 分页 -->
            <el-row>
                <el-col :span="24">
                <div class="pagination">
                    <el-pagination
                    v-if="paginations.total > 0"
                    :page-sizes="paginations.page_sizes"
                    :page-size="paginations.page_size"
                    :layout="paginations.layout"
                    :total="paginations.total"
                    :current-page.sync="paginations.page_index"
                    @current-change="handleCurrentChange"
                    @size-change="handleSizeChange"
                    ></el-pagination>
                </div>
                </el-col>
            </el-row>
        </div> 
        <el-dialog
                 title="完整日志"
                 :visible.sync="centerDialogVisible"
                 width="50%"
                 center>
                 <span>{{this.full_log}}</span>
                 <span slot="footer" class="dialog-footer">
                 <el-button @click="centerDialogVisible = false">取 消</el-button>
                 <el-button type="primary" @click="centerDialogVisible = false">确 定</el-button>
                </span>
      </el-dialog> 
    </div>

</template>
<script>

export default {
    name:'fundList',
    data(){
        return{
            tableData:[], 
            alltableData:[],
            filterTableData: [],  
            form:{
                id: "",
                hostname: "",
                name:"",
                level: "",
                full_log:"",
                timestamp:""
            },
            centerDialogVisible: false,
            //需要给分页组件传的信息
            paginations: {
                page_index: 1, // 当前位于哪页
                total: 0, // 总数
                page_size: 10, // 1页显示多少条
                page_sizes: [10 , 15, 20, 25], //每页显示多少条
                layout: "total, sizes, prev, pager, next, jumper" // 翻页属性
            },
            //筛选
            search_data: {
                startTime: "",
                endTime: ""
            }
        };
    },
    computed:{
        user() {
          return this.$store.getters.user;
    }
    },
    created(){
        this.getAlert();
    },
    methods:{
        getAlert(){
            this.$axios.get('/api/alerts').then(res => {
            console.log(res);
            this.tableData = res.data;
            this.allTableData = res.data;
            this.filterTableData = res.data;
            // // 设置分页数据
            this.setPaginations();
            }).catch(err => console.log(err));
        },        
        onDelete(index,row){
            // 删除
            this.$axios.post(`/api/alerts/delete`,{id:row.id}).then(res => {
            this.$message("删除成功");
            this.getAlert();
            });
        },
        showDetail(index,row){
            this.centerDialogVisible =true;
            this.full_log = row.full_log;
            return this.full_log;          
        },
        setPaginations() {
            // 总页数属性
            this.paginations.total = this.allTableData.length;
            this.paginations.page_index = 1;
            this.paginations.page_size = 10;
            // 设置默认分页数据
            this.tableData = this.allTableData.filter((item, index) => {
                return index < this.paginations.page_size;
            });
        },
        handleSizeChange(page_size) {
            // 切换size
            this.paginations.page_index = 1;
            this.paginations.page_size = page_size;
            this.tableData = this.allTableData.filter((item, index) => {
                return index < page_size;
            });
        },
        // 
        handleCurrentChange(page) {
            // 获取当前页
            let sortnum = this.paginations.page_size * (page - 1);
            // 数据
            let table = this.allTableData.filter((item, index) => {
                return index >= sortnum;
            });
            // 设置默认分页数据
            this.tableData = table.filter((item, index) => {
                return index < this.paginations.page_size;
            });
        },
                // 筛选
        onScreeoutMoney() {
            // 筛选
            if (!this.search_data.startTime || !this.search_data.endTime) {
                this.$message({
                    type: "warning",
                    message: "请选择时间区间"
                });
                this.getAlert();
                return;
            }
            const stime = this.search_data.startTime.getTime();
            const etime = this.search_data.endTime.getTime();
            this.allTableData = this.filterTableData.filter(item => {
                let date = new Date(item.timestamp*1000);
                let time = date.getTime();
                return time >= stime && time <= etime;
            });
            // 分页数据
            this.setPaginations();
        },
        //时间戳转日期
        time(timestamp) {
        var  date = new Date(timestamp * 1000);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
        var Y = date.getFullYear() + '-';
        var M = (date.getMonth()+1 <= 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
        var D = (date.getDate()+1 <= 10 ? '0'+(date.getDate()) : date.getDate())+' ' ;
        var h = (date.getHours()+1 <= 10 ? '0'+(date.getHours() ) : date.getHours())+ ':';
        var m = (date.getMinutes()+1 <= 10 ? '0'+(date.getMinutes() ) : date.getMinutes() )+ ':';
        var s = (date.getSeconds()+1 <= 10 ? '0'+(date.getSeconds() ) : date.getSeconds());
        return Y+M+D+h+m+s;

    }
    },
};
</script>

<style scoped>
.fillcontain {
  width: 100%;
  height: 100%;
  padding: 16px;
  box-sizing: border-box;
}
.btnRight {
  float: right;
}
.pagination {
  text-align: right;
  margin-top: 10px;
}
</style>